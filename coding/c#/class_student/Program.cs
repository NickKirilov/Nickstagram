using System;
using System.Text;

public class Student
{
	public string name;
	public string clas;
	public string id;
	private double dBel, dForeign, dMath, dPhys, dChem, dBio, average;
	public double DBel
	{
		set { this.dBel = value; }
		get { return this.dBel; }
	}
	public double DForeign
	{
		set { this.dForeign = value; }
		get { return this.dForeign; }
	}
	public double DMath
	{
		set { this.dMath = value; }
		get { return this.dMath; }
	}
	public double DPhys
	{
		set { this.dPhys = value; }
		get { return this.dPhys; }
	}
	public double DChem
	{
		set { this.dChem = value; }
		get { return this.dChem; }
	}
	public double DBio
	{
		set { this.dBio = value; }
		get { return this.dBio; }
	}
	public double Average
	{
		set { this.average = value; }
		get { return this.average; }
	}
}

namespace class_student
{
	public class Program
	{
		public static void Main(String[] args)
		{
			Console.OutputEncoding = Encoding.UTF8;
			Console.InputEncoding = Encoding.UTF8;
			Student student_one = new Student(); //here we create new object of class Students, called student_one
			Console.Write("Въведете име: "); student_one.name = Console.ReadLine(); //here we input the name of the student
			Console.Write("Въведете клас: "); student_one.clas = Console.ReadLine(); //here we input the class of the student
			Console.Write("Въведете номер: "); student_one.id = Console.ReadLine(); //here we input the id of the student
																					//here we input the marks of the student
			Console.Write("Оценка по БЕЛ: ");
			student_one.DBel = double.Parse(Console.ReadLine());
			Console.Write("Оценка по Чужд език: ");
			student_one.DForeign = double.Parse(Console.ReadLine());
			Console.Write("Оценка по Математика: ");
			student_one.DMath = double.Parse(Console.ReadLine());
			Console.Write("Оценка по Физика: ");
			student_one.DPhys = double.Parse(Console.ReadLine());
			Console.Write("Оценка по Биология: ");
			student_one.DBio = double.Parse(Console.ReadLine());
			Console.Write("Оценка по Химия: ");
			student_one.DChem = double.Parse(Console.ReadLine());
			student_one.Average = (student_one.DBel + student_one.DBio + student_one.DChem + student_one.DForeign + student_one.DMath + student_one.DPhys) / 6; //here we calculate the average mark of the student
																																								//here we print on the console the data about the given student
			Console.WriteLine("С П Р А В К А :");
			Console.WriteLine("за успеха на {0}, ученик от", student_one.name);
			Console.WriteLine("{0} клас, номер {1}", student_one.clas, student_one.id);
			Console.WriteLine("БЕЛ        - {0,4:0.00}", student_one.DBel);
			Console.WriteLine("Чужд език  - {0,4:0.00}", student_one.DForeign);
			Console.WriteLine("Математика - {0,4:0.00}", student_one.DMath);
			Console.WriteLine("Физика     - {0,4:0.00}", student_one.DPhys);
			Console.WriteLine("Химия      - {0,4:0.00}", student_one.DChem);
			Console.WriteLine("Биология   - {0,4:0.00}", student_one.DBio);
			Console.WriteLine("Ср. успех  - {0,4:0.00}", student_one.Average);
			
		}
	}


}

