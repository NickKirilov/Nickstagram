using System;

public abstract class Shape
{
    public void area()
    { }

    public void perimeter()
    { }
}

public class Circle : Shape 
{
    public int radius;
    public double Area()
    {
        return Math.PI * Math.Pow(this.radius, 2);
    }

    public double Perimeter()
    {
        return Math.PI * this.radius*2;
    }
}

public class Rectangle : Shape
{
    public double heigth;
    public double width;
    public double Area()
    {
        return this.heigth * this.width;
    }

    public double Perimeter()
    {
        return this.heigth * 2 + this.width * 2;
    }
}

namespace base_class
{
    public class Program
    {
        public static void Main(String[] args)
        {
            Circle circle = new Circle();
            circle.radius = 5;
            Console.WriteLine(circle.Area());
            //78.53981633974483 
            Console.WriteLine(circle.Perimeter());
            //31.41592653589793

            Rectangle rectangle = new Rectangle();
            rectangle.heigth = 10;
            rectangle.width = 20;
            Console.WriteLine(rectangle.Area());
            // returns 200
            Console.WriteLine(rectangle.Perimeter());
            //returns 60
        }
       
    }
}

