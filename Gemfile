source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "just-the-docs", "~> 0.10"

group :jekyll_plugins do
  gem "jekyll-sitemap"
  gem "jekyll-redirect-from"
end

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1", :install_if => Gem.win_platform?
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
