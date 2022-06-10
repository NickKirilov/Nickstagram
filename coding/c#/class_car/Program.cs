using System;
public class Car
{
	public string brand;
	public string model;
	public int engine;
	public int year;
	public double danyk;

	public void input_info()
    {
		Console.WriteLine("brand= ");
		brand = Console.ReadLine();
		Console.WriteLine("model= ");
		model = Console.ReadLine();
		Console.WriteLine("obem na dvigatelq= ");
		engine = int.Parse(Console.ReadLine());
		Console.WriteLine("godina na proizwodstwo= ");
		year = int.Parse(Console.ReadLine());
		danyk = engine * 0.2;
		if (year > 2010)
		{
			danyk += 50;
		}
		else if (year > 2000)
		{
			danyk += 60;
		}
		else
		{
			danyk += 70;
		}
		Console.WriteLine("danyk = " + danyk);
	}
	
	public void output_info()
    {
		Console.WriteLine("brand = " + brand);
		Console.WriteLine("model = " + model);
		Console.WriteLine("engine = " + engine);
		Console.WriteLine("year = " + year);
		Console.WriteLine("danyk = " + danyk);
	}
}

public class Program
{
	public static void Main()
	{
		double danyk = 0;
		Car mycar = new Car();
		mycar.input_info();
		mycar.output_info();
	}
}