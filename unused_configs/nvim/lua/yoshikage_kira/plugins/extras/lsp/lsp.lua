return {
    {
        'VonHeikemen/lsp-zero.nvim',
        dependencies = {
            {
                'williamboman/mason.nvim',
                cmd = "Mason",
                keys = { { "<leader>cm", "<cmd>Mason<cr>", desc = "Mason" } },
                build = ":MasonUpdate",
            },
            { 'williamboman/mason-lspconfig.nvim' },
            { 'neovim/nvim-lspconfig' },
            { 'folke/neodev.nvim' },
        },

        config = function()
            local lsp_zero = require('lsp-zero')
            local neodev = require('neodev')

            neodev.setup({})

            lsp_zero.on_attach(function(client, bufnr)
                lsp_zero.default_keymaps({ buffer = bufnr })
            end)

            require('mason').setup({})
            require('mason-lspconfig').setup({
                ensure_installed = { 'pyright' },
                handlers = {
                    lsp_zero.default_setup,
                },
            })

            local lspconfig = require('lspconfig')
            lspconfig.pyright.setup {}
            lspconfig.lua_ls.setup {
                settings = {
                    Lua = {
                        workspace = {
                            checkThirdParty = false,
                        },
                    },
                },
            }
        end,
    }
}
