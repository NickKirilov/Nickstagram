using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Magical_square
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            int red1, red2, red3, col1, col2, col3, dial1, dial2;
            red1 = int.Parse(textBox1.Text) + int.Parse(textBox2.Text) + int.Parse(textBox3.Text);
            red2 = int.Parse(textBox4.Text) + int.Parse(textBox5.Text) + int.Parse(textBox6.Text);
            red3 = int.Parse(textBox7.Text) + int.Parse(textBox8.Text) + int.Parse(textBox9.Text);
            col1 = int.Parse(textBox1.Text) + int.Parse(textBox4.Text) + int.Parse(textBox7.Text);
            col2 = int.Parse(textBox2.Text) + int.Parse(textBox5.Text) + int.Parse(textBox8.Text);
            col3 = int.Parse(textBox3.Text) + int.Parse(textBox6.Text) + int.Parse(textBox9.Text);
            dial1 = int.Parse(textBox1.Text) + int.Parse(textBox5.Text) + int.Parse(textBox9.Text);
            dial2 = int.Parse(textBox3.Text) + int.Parse(textBox5.Text) + int.Parse(textBox7.Text);
            label1.Text = red1.ToString();
            label2.Text = red2.ToString();
            label3.Text = red3.ToString();
            label4.Text = dial1.ToString();
            label5.Text = col3.ToString();
            label6.Text = col2.ToString();
            label7.Text = col1.ToString();
            label8.Text = dial2.ToString();
            if (red1 == 15 && red2 == 15 && red3 == 15 && dial1 == 15 && dial2 == 15 && col1 == 15 && col2 == 15 && col3 == 15)
            {
                MessageBox.Show("You win!", "Congrats!");
            }
            else if ((red1 + red2 +red3 + dial1 + dial2 + col1 + col2 + col3) > 45)
            {
                MessageBox.Show("Only the numbers between 1 and 9 may be used only once each!", "Sorry, but:");
            }
            else
            {
                MessageBox.Show("Try again!", "Sorry!");
            }


        }
    }
}
