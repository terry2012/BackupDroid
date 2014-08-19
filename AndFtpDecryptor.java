import java.security.Key;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;

class AndFtpDecryptor {
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java AndFtpDecryptor <ciphertext>");
        } else {
            String ciphertext = args[0];
            AndFtpDecryptor decryptor = new AndFtpDecryptor();
            System.out.println(decryptor.getResult(ciphertext));
        }
    }
    
    private char[] pbe_pwd;
    private byte[] pbe_salt;
    private int pbe_count;
    private String pbe_algorithm;
    private PBEParameterSpec pbe_param_spec;
    private SecretKeyFactory secret_key_factory;
    
    public AndFtpDecryptor() {
        pbe_pwd = new char[]{'P', 'B', 'E', '.', 'c', 'l', 'a', 's', 's'};
        pbe_salt = new byte[]{-57, 115, 33, -116, 126, -56, -18, -103};
        pbe_count = 30;
        pbe_algorithm = "PBEWithMD5AndDES";
        
        try {
            pbe_param_spec = new PBEParameterSpec(pbe_salt, pbe_count);
            secret_key_factory = SecretKeyFactory.getInstance(pbe_algorithm);
        } catch (Exception e) {
            
        }
    }
    
    private String getResult(String cipher_text) {
        if((cipher_text != null) && cipher_text.startsWith("{") && cipher_text.endsWith("}")) {
            byte[] binary = hex2bin(cipher_text.substring(1, cipher_text.length() - 1));
            binary = decrypt(pbe_pwd, binary, 0, binary.length);
            if(binary != null) {
                try {
                    cipher_text = new String(binary, "UTF-8");
                } catch (Exception e) {
                    
                }
            }
        }
        
        return cipher_text;
    }
    
    public byte[] hex2bin(String hex_text) {
        byte[] result = null;
        if(hex_text != null && hex_text.length() % 2 == 0) {
            int len = hex_text.length() / 2;
            result = new byte[len];
            for(int i = 0; i < len; ++i) {
                result[i] = ((byte)(Integer.parseInt(hex_text.substring(i * 2, i * 2 + 2), 16) & 255));
            }
        }

        return result;
    }

    public byte[] decrypt(char[] pbe_pwd, byte[] cipher_binary, int zero, int cipher_length) {
        byte[] result = null;
        if(cipher_binary != null) {
            try {
                SecretKey secretKey = secret_key_factory.generateSecret(new PBEKeySpec(pbe_pwd));
                Cipher cipher = Cipher.getInstance(pbe_algorithm);
                cipher.init(2, ((Key)secretKey), pbe_param_spec);
                result = cipher.doFinal(cipher_binary, zero, cipher_length);
            } catch (Exception e) {
                
            }
        }

        return result;
    }
}
