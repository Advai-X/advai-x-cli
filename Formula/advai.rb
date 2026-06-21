# Homebrew formula for advai
#
# Usage: save this file and install via a local tap:
#   1. mkdir -p "$(brew --repository)/Library/Taps/advai/homebrew-advai/Formula"
#   2. cp advai.rb "$(brew --repository)/Library/Taps/advai/homebrew-advai/Formula/advai.rb"
#   3. brew install advai
#
# To ship a new release: bump the version and replace the sha256 below.
# The sha256 can be computed with:
#   curl -sL https://pypi.io/packages/source/a/advai-cli/advai-cli-1.0.3.tar.gz | shasum -a 256

class Advai < Formula
  desc "A cross-platform CLI tool."
  homepage "https://pypi.org/project/advai-cli/"
  url "https://pypi.io/packages/source/a/advai-cli/advai-cli-1.0.3.tar.gz"
  sha256 "4195790ade2b8406d305e3e53717fcf1a9c40424a932d2002cb436943671f72f"
  license "MIT"

  depends_on "python@3.11"

  def install
    # Create a private venv, pip install the package, then symlink
    # the advai binary into the prefix so it is available on PATH.
    venv = libexec/"venv"
    system Formula["python@3.11"].opt_bin/"python3", "-m", "venv", venv
    system venv/"bin/pip", "install", "--upgrade", "pip"
    system venv/"bin/pip", "install", "."

    (bin/"advai").write_env_script venv/"bin/advai",
      PATH: "#{venv/"bin"}:$PATH"
  end

  test do
    system "#{bin}/advai", "--version"
    system "#{bin}/advai", "--help"
  end
end
