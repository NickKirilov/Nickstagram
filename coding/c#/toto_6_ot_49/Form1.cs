using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace toto_6_ot_49
{
    public partial class Form1 : Form
    {
        Random r = new Random();
        public Form1()
        {
            InitializeComponent();
        }
        int GetRandNumber()
        {
            return r.Next() % 49 + 1;
        }
        private void btn1_Click(object sender, EventArgs e)
        {
            lbl1.Text = GetRandNumber().ToString();
            lbl2.Text = GetRandNumber().ToString();
            lbl3.Text = GetRandNumber().ToString();
            lbl4.Text = GetRandNumber().ToString();
            lbl5.Text = GetRandNumber().ToString();
            lbl6.Text = GetRandNumber().ToString();

        }
    }
}
