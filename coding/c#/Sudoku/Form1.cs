using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Sudoku
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            if (comboBox1.Text == "easy")
            {
                textBox1.Text = "9";
                textBox3.Text = "4";

            }
        }

        private void label3_Click(object sender, EventArgs e)
        {

        }
    }
}
