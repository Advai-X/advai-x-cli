# Homebrew 配方 — 发布到你自己的 tap 仓库（homebrew-advai）后即可：
#   brew tap Advai-X/advai
#   brew install advai
#
# 注意：
#   1) url 请替换为你 GitHub Releases 下对应版本的 tar.gz 下载地址
#   2) sha256 需要在每次发布新版本时用 `shasum -a 256 xxx.tar.gz` 重新计算
#   3) 本配方依赖 python@3（系统自带或 brew 安装的 python3 都可）
#
# 推荐发布流程：
#   a. 在 GitHub 打 tag v1.0.0 并生成 Release，附带源码 tar.gz
#   b. 用 `brew create --tap Advai-X/advai https://.../v1.0.0.tar.gz` 生成骨架
#   c. 把本文件内容拷进 homebrew-advai/Formula/advai.rb 并 push

class Advai < Formula
  include Language::Python::Virtualenv

  desc "跨平台 AI Skill 管理器 — 一键 install / uninstall / list / update"
  homepage "https://github.com/Advai-X/advai-x-cli"
  url "https://github.com/Advai-X/advai-x-cli/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256_OF_THE_TARBALL"
  license "MIT"
  version "1.0.0"

  depends_on "python@3.11"

  resource "click" do
    url "https://files.pythonhosted.org/packages/59/87/84326af34517fca8c58418d148f2403df25303e02736832403587318e9e8/click-8.1.3.tar.gz"
    sha256 "7682dc8afb30297001674575ea00d1814d808d6a36af415a82bd481d37ba7b8e"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/advai", "--version"
    system "#{bin}/advai", "--help"
  end
end
