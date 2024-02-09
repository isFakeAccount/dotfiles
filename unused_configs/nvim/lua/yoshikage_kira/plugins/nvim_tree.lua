return {
    'nvim-tree/nvim-tree.lua',
    dependencies = {
        'nvim-tree/nvim-web-devicons',
    },

    config = function()
        vim.g.loaded_netrw = 1
        vim.g.loaded_netrwPlugin = 1

        vim.keymap.set("n", "<leader>e", ":NvimTreeToggle<cr>", { desc = "nvim-tree - Toggle" })
        require("nvim-tree").setup({
            filters = {
                dotfiles = false,
            },
            git = {
                enable = true,
                ignore = false,
                timeout = 500,
            },
        })
    end
}
