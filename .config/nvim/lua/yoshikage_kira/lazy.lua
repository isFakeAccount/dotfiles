local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  -- bootstrap lazy.nvim
  -- stylua: ignore
  vim.fn.system({ "git", "clone", "--filter=blob:none", "https://github.com/folke/lazy.nvim.git", "--branch=stable",
    lazypath })
end
vim.opt.rtp:prepend(vim.env.LAZY or lazypath)

require("lazy").setup({
  { import = "yoshikage_kira.plugins" },
  { import = "yoshikage_kira.plugins.extras.dap" },
  { import = "yoshikage_kira.plugins.extras.formatting" },
  { import = "yoshikage_kira.plugins.extras.lang" },
  -- { import = "yoshikage_kira.plugins.extras.linting" },
  { import = "yoshikage_kira.plugins.extras.lsp" },
  { import = "yoshikage_kira.plugins.extras.ui" },
  { import = "yoshikage_kira.plugins.extras.utils" },
}, {
  check = {
    enabled = true,
    notify = false,
  },
})
