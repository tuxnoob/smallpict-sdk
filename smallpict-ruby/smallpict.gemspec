# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "smallpict"
  spec.version       = "0.1.0.pre.1"
  spec.authors       = ["SmallPict Engineering"]
  spec.email         = ["support@tuxnoob.com"]

  spec.summary       = "Official Ruby gem for SmallPict Image Optimization API"
  spec.description   = "High-performance image transcoding and optimization gem with Rails ActiveStorage support."
  spec.homepage      = "https://smallpict.tuxnoob.com"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 3.0.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = "https://github.com/tuxnoob/smallpict-ruby"
  spec.metadata["changelog_uri"] = "https://github.com/tuxnoob/smallpict-ruby/blob/main/CHANGELOG.md"

  spec.files = Dir["lib/**/*.rb", "README.md", "LICENSE", "SECURITY.md"]
  spec.require_paths = ["lib"]

  spec.add_dependency "faraday", ">= 2.0"
  spec.add_development_dependency "rspec", "~> 3.12"
  spec.add_development_dependency "webmock", "~> 3.18"
  spec.add_development_dependency "rubocop", "~> 1.50"
end
