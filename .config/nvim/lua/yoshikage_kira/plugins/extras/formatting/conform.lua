return {
    'stevearc/conform.nvim',
    event = { "BufReadPre", "BufNewFile" },
    cmd = "ConformInfo",
    keys = {
        {
            "<leader>cf",
            function()
                require("conform").format({
                    lsp_fallback = true,
                    async = false,
                    timeout_ms = 500,
                })
            end,
            mode = { "n", "v" },
            desc = "Format file or range (in visual mode)",
        },
    },
    config = function()
        local conform = require("conform")

        conform.setup({
            formatters_by_ft = {
                python = { "isort", "black" },
            },
        })
    end
}
