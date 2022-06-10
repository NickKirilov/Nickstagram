using system;
class bezkrainost{
    static void Main(){
        console.writeline("Calculate ht infinite sum:\n");
        double x,zn,ch,a,i,s,eps;
        do{
            {Console.Write("Enter x>0 and x<1, x=");
            x = double.Parse(Console.ReadLine());
        } while ((x>=1) || (x<=0));
        do{
            Console.Write("Enter eps>0 and eps<=0.1, It defines the precision: eps=");
            eps = double.Parse(Console.ReadLine());
        } while ((eps>0.1) || (eps<=0));
        i=1.0; 
        ch=x; 
        zn=1.0; 
        a=ch/zn; 
        s=1.0; 
        do{ 
            Console.Write("s="+s+"+"+ch+"/"+zn+"=");
        s=s+a; 
        Console.WriteLine(s);
        ch=ch*x;
        i=i+1.0;
        zn=zn*i;
        a=ch/zn;
        } while (a>=eps);
    }

}