# Apache Sanal Sunucu Yöneticisi
## Windows üzerinde koşulan Apache sunucusuna ait sanal sunucuları yönetir.

version: v.0.2

Bu programı kullanabilmeniz için Apache üzerinde yapmanız gereken bazı ayarlamalar var. Öncelikle `Apache/conf/httpd.conf` dosyasında `#Include conf/extra/httpd-vhosts.conf` satırındaki `#` işaretini kaldırarak sanal sunucuları aktif hale getirmeniz gerekiyor.

Daha sonra `Apache/conf` klasörünün içerisine `virtualhosts` adında bir klasör oluşturmanız gerekiyor.

Son olarak `Apache/conf/extra/httpd-vhosts.conf` dosyasının içeriğini silerek aşağıdaki kodları yapıştırmanız gerekiyor.

```
# Virtual Hosts
#
# Required modules: mod_log_config
Include conf/virtualhosts/*.conf
```

Doğrudan `sanalsunucu.py` dosyasını python ile kullanırsanız `hosts` dosyasının üzerine yazamadığı için program hata veriyor. pyinstaller ile sanalsunucu.py dosyasını .exe ye çevirmeniz gerekiyor. pyinstaller komutunu kullanmadan önce gerekli kütüphanelerin yüklenmesi için şu komutu çalıştırın:
```
pip install -r req.txt
```
Gerekli kütüphaneler kurulduktan sonra `pyinstaller_usage.txt` dosyasının içindeki kodu, yolları düzenleyerek cmd üzerinde çalıştırın. Bulunduğunuz klasörde `dist` adında bir klasör oluşacaktır. Bu klasörün içindeki sanalsunucu klasörünü bir dizine kopyalayın ve içerisindeki sanalsunucu.exe dosyasını çalıştırın. İlk kullanımda Apache klasörünüzün yolunu ve sitelerinizi barındıracağınız klasörün adını soracaktır. Bunları verdikten sonra windows üzerinde rahatlıkla sanal sunucu oluşturup kullanabilirsiniz.

Antivirüs programı kullanan kişiler programda `sanalsunucu.exe` dosyasını güvenilir olarak işaretlemeniz gerekmektedir yoksa hosts dosyasına yazma yapamıyor. exe dosyasınız dijital olarak imzalanmadığı için özellikle kaspersky güvenilmez yazılım olarak kabul ediyor. Program admin yetkileriyle çalışsa da hosts dosyasına yazamıyorsa hosts dosyasının güvenlik izinlerini herkesin yazabileceği şekilde değiştirmeniz gerekebilir.

hosts dosyası Windows üzerinde aşağıdaki klasörde bulunuyor.

```
C:\Windows\System32\drivers\etc
```

Not: Apache son sürümlerinde virtual host dosyasında bazı değişikliklere gittiği için sanalsunucu.py dosyasında ufak bir güncelleme yapıldı. O yüzden setup dosyası kaldırıldı. pyinstaller ile kendi exenizi yapıp çalıştırın. İleride belki yeni bir installer oluştururum.

## License
MIT

**Free Software!**
