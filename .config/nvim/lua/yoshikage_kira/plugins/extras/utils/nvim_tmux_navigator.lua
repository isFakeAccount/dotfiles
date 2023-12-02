return {
    "alexghergh/nvim-tmux-navigation",
    config = function()
        local nvim_tmux_nav = require('nvim-tmux-navigation')

        nvim_tmux_nav.setup {
            disable_when_zoomed = true
        }

        vim.keymap.set('n', "<C-h>", nvim_tmux_nav.NvimTmuxNavigateLeft)
        vim.keymap.set('n', "<C-j>", nvim_tmux_nav.NvimTmuxNavigateDown)
        vim.keymap.set('n', "<C-k>", nvim_tmux_nav.NvimTmuxNavigateUp)
        vim.keymap.set('n', "<C-l>", nvim_tmux_nav.NvimTmuxNavigateRight)
        vim.keymap.set('n', "<C-\\>", nvim_tmux_nav.NvimTmuxNavigateLastActive)
        vim.keymap.set('n', "<C-Space>", nvim_tmux_nav.NvimTmuxNavigateNext)
        
	-- Resize windows using Alt + hjkl
	vim.keymap.set('n', '<M-h>', ':vertical resize -2<CR>', { noremap = true, silent = true })
	vim.keymap.set('n', '<M-l>', ':vertical resize +2<CR>', { noremap = true, silent = true })
	vim.keymap.set('n', '<M-j>', ':resize -2<CR>', { noremap = true, silent = true })
	vim.keymap.set('n', '<M-k>', ':resize +2<CR>', { noremap = true, silent = true })

    end
}
