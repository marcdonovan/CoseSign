using System.Security.Cryptography;
using System.Text;
using Microsoft.Cose;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 3)
        {
            Console.WriteLine("Usage: CoseSigner <inputFile> <outputFile> <privateKeyFile>");
            return;
        }

        var inputFile = args[0];
        var outputFile = args[1];
        var privateKeyFile = args[2];

        var content = File.ReadAllBytes(inputFile);
        var keyBytes = File.ReadAllBytes(privateKeyFile);
        using var key = ECDsa.Create();
        key.ImportPkcs8PrivateKey(keyBytes, out _);

        var signer = new CoseMessage
        {
            Content = content,
        };

        signer.Protect(key, CoseAlgorithm.ES256);
        File.WriteAllBytes(outputFile, signer.Encode());
        Console.WriteLine($"File signed: {outputFile}");
    }
}
