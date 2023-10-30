return {
    "folke/which-key.nvim",
    event = "VeryLazy",
    init = function()
        vim.o.timeout = true
        vim.o.timeoutlen = 300
    end,
    opts = {
        window = {
            border = "single",        -- none, single, double, shadow
            position = "bottom",      -- bottom, top
            margin = { 0, 0, 0, 0 },  -- extra window margin [top, right, bottom, left]. When between 0 and 1, will be treated as a percentage of the screen size.
            padding = { 0, 0, 0, 0 }, -- extra window padding [top, right, bottom, left]
            winblend = 0,             -- value between 0-100 0 for fully opaque and 100 for fully transparent
            zindex = 1000,            -- positive value to position WhichKey above other floating windows.
        },
        layout = {
            height = { min = 4, max = 20 }, -- min and max height of the columns
            width = { min = 50, max = 70 }, -- min and max width of the columns
            spacing = 1,                    -- spacing between columns
            align = "left",                 -- align columns left, center or right
        },
    },
    config = function(_, opts)
        local wk = require("which-key")
        wk.setup(opts)
        wk.register(opts.default)
        wk.register({
            ["g"] = { name = "+goto" },
            ["<S-k>"] = "lookup Keyword under the cursor with 'keywordprg'",
            ["]"] = { name = "+next" },
            ["["] = { name = "+prev" },
            ["<leader>c"] = { name = "+code" },
            ["<leader>f"] = { name = "+file/find" },
            ["<leader>d"] = { name = "+dap" },
        })
    end,
}
