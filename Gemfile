source "https://rubygems.org"

# Jekyll and the Just-the-Docs theme.  Pinned to the GitHub Pages
# compatible Jekyll 3.x line so that local builds match production.
gem "jekyll", "~> 3.10"
gem "just-the-docs"

group :jekyll_plugins do
  gem "jekyll-sitemap"
  gem "jekyll-redirect-from"
  gem "jekyll-seo-tag"
  gem "jekyll-remote-theme"
end

# Markdown processor used by GitHub Pages.
gem "kramdown-parser-gfm"

# Windows and JRuby do not include zoneinfo files; bundle the tzinfo-data
# gem and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance booster for watching directories on Windows.
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# HTTP server adapter required by Ruby 3.x.
gem "webrick", "~> 1.8"

# CSV gem is no longer in the default gem set on Ruby 3.4+.
gem "csv"
