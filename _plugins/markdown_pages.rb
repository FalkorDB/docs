# frozen_string_literal: true

# markdown_pages.rb
#
# Emits a clean Markdown version of every documentation page so AI tools
# (and humans) can fetch the raw content.
#
# For a page rendered at <url>.html (or a "pretty" URL like <url>/), this
# plugin writes a sibling file at <url>.md containing only the page body
# (front matter, layouts, navigation, footer and other site chrome are
# excluded).  Liquid tags and `{% include %}` directives are expanded so
# the output is self-contained markdown.
#
# Usage notes
# -----------
# * A page can opt out by setting `markdown_skip: true` in its front
#   matter.
# * Pages with `layout: redirect` are skipped automatically.
# * The plugin also writes `_site/.well-known/markdown-index.txt`, a
#   newline-separated list of every emitted markdown URL, useful for
#   crawlers and AI ingestion pipelines.
#
# Content negotiation
# -------------------
# This plugin produces static `.md` files only.  Honouring an
# `Accept: text/markdown` request header requires server/CDN logic
# (for example, a Cloudflare Worker or Netlify `_redirects` rule that
# rewrites the request to the `.md` URL when the header is present).
# A reference Cloudflare Worker is shipped at
# `markdown-content-negotiation.worker.js` in the repository root.

require "fileutils"

module FalkorDocs
  module MarkdownPages
    SKIP_LAYOUTS = %w[redirect].freeze

    module_function

    # Compute the on-disk path (inside `site.dest`) for the markdown
    # version of a page given its rendered URL.
    def target_path(site, url)
      return File.join(site.dest, "index.md") if url.nil? || url == "/" || url.empty?

      if url.end_with?("/")
        File.join(site.dest, url, "index.md")
      elsif url.end_with?(".html")
        File.join(site.dest, url.sub(/\.html\z/, ".md"))
      else
        File.join(site.dest, "#{url}.md")
      end
    end

    # Compute the public URL where the markdown version is served.
    def target_url(url)
      return "/index.md" if url.nil? || url == "/" || url.empty?

      if url.end_with?("/")
        "#{url}index.md"
      elsif url.end_with?(".html")
        url.sub(/\.html\z/, ".md")
      else
        "#{url}.md"
      end
    end

    def eligible?(page)
      return false unless page.path.end_with?(".md", ".markdown")
      return false if page.data["markdown_skip"]
      return false if SKIP_LAYOUTS.include?(page.data["layout"].to_s)
      return false if page.url.to_s.end_with?(".md")

      true
    end

    # Render the page's source content through Liquid only (no Markdown
    # conversion) and write the result to disk.  We re-read the source
    # file from disk because by the time the `:site, :post_write` hook
    # runs Jekyll has already mutated `page.content` in place to be the
    # converted HTML output.
    def write(site, page)
      out_path = target_path(site, page.url)
      FileUtils.mkdir_p(File.dirname(out_path))

      source = read_source(page)

      payload = site.site_payload.merge(
        "page"            => page.to_liquid,
        "markdown_format" => true,
      )
      info = {
        registers:        { site: site, page: page.to_liquid },
        strict_filters:   false,
        strict_variables: false,
      }

      rendered =
        begin
          template = site.liquid_renderer.file("#{page.path}.md").parse(source)
          template.render!(payload, info)
        rescue StandardError => e
          Jekyll.logger.warn("MarkdownPages:",
                             "Liquid render failed for #{page.path}: #{e.message}")
          source
        end

      File.write(out_path, rendered)
      target_url(page.url)
    end

    # Read the original markdown source from disk and strip the YAML
    # front matter block.  Anything between the leading `---` markers is
    # site chrome metadata (title, layout, nav order, etc.) and not
    # part of the page body.
    def read_source(page)
      raw = File.read(File.join(page.site.source, page.relative_path))
      if raw =~ /\A---\s*\n.*?\n---\s*\n/m
        raw.sub(/\A---\s*\n.*?\n---\s*\n/m, "").lstrip
      else
        raw
      end
    end

    # Write a manifest of every emitted markdown URL.
    def write_index(site, urls)
      return if urls.empty?

      index_path = File.join(site.dest, ".well-known", "markdown-index.txt")
      FileUtils.mkdir_p(File.dirname(index_path))
      base = (site.config["url"] || "").sub(%r{/\z}, "")
      lines = urls.sort.uniq.map { |u| "#{base}#{u}" }
      File.write(index_path, "#{lines.join("\n")}\n")
    end
  end
end

Jekyll::Hooks.register :site, :post_write do |site|
  emitted = []
  site.pages.each do |page|
    next unless FalkorDocs::MarkdownPages.eligible?(page)

    emitted << FalkorDocs::MarkdownPages.write(site, page)
  end
  FalkorDocs::MarkdownPages.write_index(site, emitted)
  Jekyll.logger.info("MarkdownPages:",
                     "wrote #{emitted.size} markdown page(s)")
end
