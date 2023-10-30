return {
    {
        'mfussenegger/nvim-dap',
        event = "VeryLazy",
        dependencies = {
            'rcarriga/nvim-dap-ui',
            'jay-babu/mason-nvim-dap.nvim',
            'theHamsta/nvim-dap-virtual-text',
        },

        keys = {
            {
                "<leader>dB",
                function() require("dap").set_breakpoint(vim.fn.input("Breakpoint condition: ")) end,
                desc = "Breakpoint Condition",
            },
            {
                "<leader>db",
                function() require("dap").toggle_breakpoint() end,
                desc = "Toggle Breakpoint",
            },
            {
                "<leader>dc",
                function()
                    require("dap").continue()
                    vim.cmd('NvimTreeClose')
                end,
                desc = "Continue",
            },
            {
                "<leader>dC",
                function() require("dap").run_to_cursor() end,
                desc = "Run to Cursor",
            },
            {
                "<leader>dg",
                function() require("dap").goto_() end,
                desc = "Go to line (no execute)",
            },
            {
                "<leader>di",
                function() require("dap").step_into() end,
                desc = "Step Into",
            },
            {
                "<leader>dd",
                function() require("dap").down() end,
                desc = "Down",
            },
            {
                "<leader>du",
                function() require("dap").up() end,
                desc = "Up",
            },
            {
                "<leader>dl",
                function() require("dap").run_last() end,
                desc = "Run Last",
            },
            {
                "<leader>do",
                function() require("dap").step_out() end,
                desc = "Step Out",
            },
            {
                "<leader>dO",
                function() require("dap").step_over() end,
                desc = "Step Over",
            },
            {
                "<leader>dp",
                function() require("dap").pause() end,
                desc = "Pause",
            },
            {
                "<leader>dr",
                function() require("dap").repl.toggle() end,
                desc = "Toggle REPL",
            },
            {
                "<leader>ds",
                function() require("dap").session() end,
                desc = "Session",
            },
            {
                "<leader>dt",
                function() require("dap").terminate() end,
                desc = "Terminate",
            },
            {
                "<leader>dw",
                function() require("dap.ui.widgets").hover() end,
                desc = "Widgets",
            },
        },

        config = function(_, opts)
            local dap = require('dap')
            local dapui = require('dapui')

            require('mason-nvim-dap').setup {
                automatic_setup = true,
                handlers = {},
                ensure_installed = {},
            }

            -- Basic debugging keymaps --

            vim.keymap.set('n', '<F2>', dap.step_into, { desc = 'Debug: Step Into' })
            vim.keymap.set('n', '<F3>', dap.step_over, { desc = 'Debug: Step Over' })
            vim.keymap.set('n', '<F4>', dap.step_out, { desc = 'Debug: Step Out' })
            vim.keymap.set('n', '<F5>', function()
                dap.continue()
                vim.cmd('NvimTreeClose')
            end, { desc = 'Debug: Start/Continue' })

            vim.keymap.set('n', '<F6>', function() require('dap').repl.open() end, { desc = 'REPL Open' })
            vim.keymap.set('n', '<F7>', dap.toggle_breakpoint, { desc = 'Debug: Toggle Breakpoint' })
            vim.keymap.set('n', '<F8>', function()
                dap.set_breakpoint(vim.fn.input('Breakpoint condition: '))
            end, { desc = 'Debug: Set Breakpoint' })

            vim.keymap.set('n', '<Leader>dl', function() require('dap').run_last() end)
            -- Toggle to see last session result. Without this, you can't see session output in case of unhandled exception.
            vim.keymap.set('n', '<F12>', function()
                dapui.toggle()
                vim.cmd('NvimTreeToggle')
            end, { desc = 'Debug: See last session result.' })

            -- Dap UI setup
            dapui.setup {
                icons = { expanded = '▾', collapsed = '▸', current_frame = '*' },
                controls = {
                    icons = {
                        pause = '⏸',
                        play = '▶',
                        step_into = '⏎',
                        step_over = '⏭',
                        step_out = '⏮',
                        step_back = 'b',
                        run_last = '▶▶',
                        terminate = '⏹',
                        disconnect = '⏏',
                    },
                },
            }


            dap.listeners.after.event_initialized['dapui_config'] = dapui.open
            dap.listeners.before.event_terminated['dapui_config'] = dapui.close
            dap.listeners.before.event_exited['dapui_config'] = dapui.close

            require("nvim-dap-virtual-text").setup()
        end,
    },
}
