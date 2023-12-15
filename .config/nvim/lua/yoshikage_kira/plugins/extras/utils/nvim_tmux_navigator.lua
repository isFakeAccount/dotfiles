return {
    "alexghergh/nvim-tmux-navigation",
    config = function()
        local nvim_tmux_nav = require('nvim-tmux-navigation')

        nvim_tmux_nav.setup {
            disable_when_zoomed = true
        }

	vim.keymap.set('n', "<C-h>", nvim_tmux_nav.NvimTmuxNavigateLeft, { noremap = true, silent = true, desc = "Navigate Left in tmux" })
	vim.keymap.set('n', "<C-j>", nvim_tmux_nav.NvimTmuxNavigateDown, { noremap = true, silent = true, desc = "Navigate Down in tmux" })
	vim.keymap.set('n', "<C-k>", nvim_tmux_nav.NvimTmuxNavigateUp, { noremap = true, silent = true, desc = "Navigate Up in tmux" })
	vim.keymap.set('n', "<C-l>", nvim_tmux_nav.NvimTmuxNavigateRight, { noremap = true, silent = true, desc = "Navigate Right in tmux" })
	vim.keymap.set('n', "<C-\\>", nvim_tmux_nav.NvimTmuxNavigateLastActive, { noremap = true, silent = true, desc = "Navigate to Last Active Pane in tmux" })
	vim.keymap.set('n', "<C-Space>", nvim_tmux_nav.NvimTmuxNavigateNext, { noremap = true, silent = true, desc = "Navigate to Next Pane in tmux" })


        -- Resize windows using Alt + hjkl
        vim.keymap.set('n', '<M-h>', ':vertical resize -2<CR>', { noremap = true, silent = true })
        vim.keymap.set('n', '<M-l>', ':vertical resize +2<CR>', { noremap = true, silent = true })
        vim.keymap.set('n', '<M-j>', ':resize -2<CR>', { noremap = true, silent = true })
        vim.keymap.set('n', '<M-k>', ':resize +2<CR>', { noremap = true, silent = true })

    end
}
