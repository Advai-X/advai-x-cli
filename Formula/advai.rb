# Homebrew formula for advai — usage:
#
#   # Recommended (standard tap flow):
#   brew tap Advai-X/advai https://github.com/Advai-X/advai-x-cli
#   brew install advai
#
#   # Alternative: install from the local formula file:
#   curl -fsSL https://cdn.jsdelivr.net/gh/Advai-X/advai-x-cli@main/Formula/advai.rb \
#     > "$(brew --repository)/Library/Taps/advai-x/homebrew-advai/Formula/advai.rb"
#   brew install advai
#
# To ship a new release, bump the version and sha256 below.

class Advai < Formula
  desc "Cross-platform AI Skill manager — one-click install / uninstall / list / update"
  homepage "https://github.com/Advai-X/advai-x-cli"
  url "https://github.com/Advai-X/advai-x-cli/archive/refs/tags/v1.0.1.tar.gz"
  sha256 "22fcb0cd36f6d3d6ddbce28beb2942095710cc30e015113b287685cf466142b9"
  license "MIT"

  depends_on "python@3.11"

  def install
    # Create a private venv and pip-install the package, then symlink
    # `bin/advai` so it is available on the user's PATH after `brew install`.
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
