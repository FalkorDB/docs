module Jekyll
  class MarkdownExporter < Generator
    safe false
    priority :low

    def generate(site)
      site.pages.each do |page|
        next unless page.name.end_with?(".md")

        dest_path = File.join(site.dest, page.url + ".md")
        FileUtils.mkdir_p(File.dirname(dest_path))
        File.write(dest_path, page.content)
      end
    end
  end
end
