using System;
class DecToBinaryRec
    {     
        static void DecToBinRec(int n)
        {
            if(n==0)
        {
            Console.Write("");
            return;
        }
        DecToBinRec(n / 2);
        Console.Write(n % 2);
        }
       static public void Main()
        {
            Console.Write("n=");
            int n = int.Parse(Console.ReadLine());
            DecToBinRec(n);
        }
}

