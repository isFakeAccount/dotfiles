return {
    'akinsho/bufferline.nvim',
    version = "*",
    dependencies = 'nvim-tree/nvim-web-devicons',
    config = function()
        require("bufferline").setup {
            options = {
                diagnostics = "nvim_lsp",
                offsets = {
                    {
                        filetype = "NvimTree",
                        text = function()
                            return vim.fn.fnamemodify(vim.fn.getcwd(), ":t")
                        end,
                        highlight = "Directory",
                        separator = true,
                    }
                }
            }
        }
    end,
}
