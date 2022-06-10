using System;
namespace BinomCoef
{
    class BinCoef
    {
        static double vasko(int n, int k)
        {
            if (k == 0 || k == n) return 1;
            else {
                return vasko(n - 1, k - 1);
                return vasko(n - 1, k);
            }
        }
        static void Main()
        {
            Console.Write("n=");
            int n = int.Parse(Console.ReadLine());
            Console.Write("k=");
            int k = int.Parse(Console.ReadLine());
            vasko(n, k);
            Console.Write(n+k);
            
        }
    }
}