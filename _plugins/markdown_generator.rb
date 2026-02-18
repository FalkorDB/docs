# Jekyll plugin to generate .md versions of documentation pages for AI tools
# This creates clean markdown files at URL.md for each documentation page

module Jekyll
  class MarkdownPageGenerator < Generator
    safe true
    priority :lowest

    def generate(site)
      # Collect all pages that should have .md versions
      pages_to_process = []

      site.pages.each do |page|
        # Only process markdown source files
        next unless page.name.end_with?('.md')

        # Skip if already a .md URL endpoint
        next if page.url.end_with?('.md')

        # Skip special files
        next if page.name.start_with?('_')

        pages_to_process << page
      end

      # Generate .md versions
      pages_to_process.each do |source_page|
        md_page = MarkdownPage.new(site, source_page)
        site.pages << md_page
      end
    end
  end

  class MarkdownPage < Page
    def initialize(site, source_page)
      @site = site
      @base = site.source
      @dir = File.dirname(source_page.relative_path)

      # Generate unique name for .md version
      base_name = File.basename(source_page.name, '.md')
      @name = "#{base_name}.source.md"

      # Process the filename
      self.process(@name)

      # Copy and modify data
      self.data = {}
      self.data['layout'] = 'markdown'
      self.data['title'] = source_page.data['title']
      self.data['description'] = source_page.data['description']

      # Set permalink to be original_url.md
      base_url = source_page.url.chomp('/')
      base_url = '/' if base_url.empty?
      self.data['permalink'] = "#{base_url}.md"

      # Get the content
      self.content = source_page.content
    end
  end
end
