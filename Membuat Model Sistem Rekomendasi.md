# LAPORAN PROYEK *MACHINE LEARNING* - DWI NUR AGUSTINA
#
#

## Project Overview
Semakin berkembangnya teknologi akan diiringi dengan semakin banyaknya informasi yang tersedia. Pencarian informasi menggunakan internet akan semakin sulit karena terlalu banyak informasi yang tersedia. Dahulu, informasi hanya terdapat di media cetak. Namun, semakin berkembangnya teknologi informasi mulai berpindah ke media elektronik. Saat ini dengan adanya teknologi internet, hampir semua informasi yang dibutuhkan sudah tersedia di internet dengan berbagai versi yang terkadang membingungkan karena informasi yang tersedia terlalu banyak. Hal yang sama juga terjadi pada informasi yang berkaitan dengan film.

Menurut *British Film Institute (BFI)*, film *box office* yang diproduksi terus meningkat setiap tahunnya mulai tahun 2009 hingga tahun 2015. Pada tahun 2009 terdapat 503 film yang diproduksi dan pada tahun 2015 terdapat sebanyak 759 film yang diproduksi. Tidak jarang seseorang yang ingin menonton film menjadi kebingungan karena terlalu banyak film yang tersedia di internet. Oleh karena itu, dibutuhkan sebuah sistem yang dapat membantu memberikan informasi yang sesuai dengan keinginan *user*. Sistem tersebut sering disebut dengan sistem rekomendasi. Sistem rekomendasi adalah suatu teknologi yang didesain untuk mempermudah *user* dalam menemukan suatu data yang mungkin sesuai dengan profil *user* secara cepat dan dapat mengurangi jumlah informasi yang terlalu banyak. Terdapat beberapa algoritma yang dapat dipakai untuk membangun sistem rekomendasi dengan kelebihan dan kekurangan masing-masing. Salah satu algoritma sistem rekomendasi yang paling banyak digunakan adalah *collaborative filtering*.

#
## Business Understanding
#### 1. Problem Statements
Berdasarkan latar belakang di atas, maka dapat dirumuskan permasalahan sebagai berikut:
* Bagaimana cara membuat *user experience* meningkat ketika mencari *movie* yang akan ditonton?
* Bagaimana cara membuat sistem rekomendasi *movie* dengan menggunakan pendekatan *collaborative filtering*?
#
#### 2. Goals
Proyek ini dilakukan dengan tujuan sebagai berikut:
* Dapat meningkatkan *user experience* saat akan mencari *movie* yang ingin ditonton
* Dapat mengimplementasikan pendekatan *collaborative filtering* untuk membuat sistem rekomendasi *movie*
#
#### 3. Solution Statements
Dari rumusan masalah dan tujuan yang telah diuraikan, solusi yang dapat dilakukan adalah sebagai berikut:
Menggunakan pendekatan *collaborative filtering* untuk membuat sistem rekomendasi *movie*, dikarenakan dataset yang digunakan hanya berisi tentang *rating user* dan *genre* film. Pada *collaborative filtering*, atribut yang digunakan bukan konten tetapi *user behaviour*. Contohnya, ketika merekomendasikan suatu item berdasarkan riwayat *rating* dari *user* tersebut maupun *user* lain.
#
## Data Understanding
Dataset yang digunakan pada proyek ini adalah dataset yang diambil dari *website* https://www.kaggle.com/ lebih tepatnya yaitu https://www.kaggle.com/datasets/shubhammehta21/movie-lens-small-latest-dataset dengan nama dataset adalah *Movie Lens Small Latest Dataset*. Dimana dataset yang digunakan memiliki format .csv dan didalamnya terdapat 4 file .csv. Namun, pada proyek kali ini hanya menggunakan 3 file .csv tersebut. Untuk lebih jelasnya adalah sebagai berikut:
1. movies.csv terdapat 9742 baris dan 3 kolom, dengan penjelasan kolom sebagai berikut:
* movieId : merupakan unique Id yang disediakan untuk setiap film
* title : merupakan nama film dengan tahun dalam tanda kurung
* genres : merupakan genre pada film tersebut
#
2. ratings.csv terdapat 100836 baris dan 4 kolom, dengan penjelasan kolom sebagai berikut:
* userId : merupakan unique Id yang disediakan untuk setiap user
* movieId : merupakan unique Id yang disediakan untuk setiap film
* rating : merupakan penilaian user terhadap film terkait
* timestamp : merupakan kode waktu film
#
3. tags.csv terdapat 3683 baris dan 4 kolom, dengan penjelasan kolom sebagai berikut:
* userId : merupakan unique Id yang disediakan untuk setiap user
* movieId : merupakan unique Id yang disediakan untuk setiap film
* tag : merupakan metadata yang dibuat user tentang film
* timestamp : merupakan kode waktu film

Untuk *overview* dari dataset tersebut setelah dijadikan *dataframe* adalah sebagai berikut:

movie_df : yang berisi dataset movies.csv yang ditunjukkan pada Tabel 1.

Tabel 1. *Overview* movie_df
| movieId | title	                                     | genres                                      |
|---------|--------------------------------------------|---------------------------------------------|
| 1       | Toy Story (1995)                           | Adventure|Animation|Children|Comedy|Fantasy |
| 2       | Jumanji (1995)                             | Adventure|Children|Fantasy                  |
| 3       | Grumpier Old Men (1995)	                   | Comedy|Romance                              |
| 4       | Waiting to Exhale (1995)	                 | Comedy|Drama|Romance                        |
| 5       | Father of the Bride Part II (1995)	       | Comedy                                      |
| ......  | ...........................................|............................................ |
| 193581  | Black Butler: Book of the Atlantic (2017)  | Action|Animation|Comedy|Fantasy             |
| 193583	| No Game No Life: Zero (2017)               | Animation|Comedy|Fantasy                    |
| 193585  | Flint (2017)		                           | Drama                                       |
| 193587  | Bungo Stray Dogs: Dead Apple (2018)		     | Action|Animation                            |
| 193609  | Andrew Dice Clay: Dice Rules (1991)		     | Comedy                                      |

#
rating_df : yang berisi dataset ratings.csv yang sudah didelete kolom timestampnya yang ditunjukkan pada Tabel 2.

Tabel 2. *Overview* rating_df
| userId | movieId | rating |
|--------|---------|--------|
| 1	     | 1	     | 4.0    |
| 1	     | 3	     | 4.0    |
| 1	     | 6	     | 4.0    |
| ...... | ....... | ...... |
| 610    | 168250  | 5.0    |
| 610    | 168252  | 5.0    |
| 610    | 170875  | 3.0    |

#
tags_df : yang berisi dataset tags.csv yang ditunjukkan pada Tabel 3.

Tabel 3. *Overview* tags_df
| userId | movieId | tag              | timestamp  | 
|--------|---------|------------------| ---------- |
| 2	     | 60756	 | funny            | 1445714994 |
| 2	     | 60756	 | Highly quotable  | 1445714996 |
| 2	     | 60756	 | will ferrel      | 1445714992 |
| ...... | ....... | ................ | .......... |
| 610	   | 3265	   | gun fu           | 1493843984 |
| 610	   | 3265	   | heroic Bloodshed | 1493843978 |
| 610    | 168248	 | Heroic Bloodshed | 1493844270 |

#
## Data Preparation
Teknik *data preparation* yang digunakan ada beberapa cara. Dimana terdapat 3 dataframe yang akan diperiksa dan disiapkan yaitu movie_df, rating_df, dan tags_df. Berikut merupakan penjelasan beberapa teknik yang digunakan untuk *data preparation* pada proyek kali ini:
1. Removing missing value:
Tahapan ini diperlukan karena dengan tidak adanya *missing value* akan membuat performa dalam pembuatan model menjadi lebih baik. Tahapan ini dilakukan dengan kode "dataframe.dropna()". Kode tersebut berfungsi untuk menghapuskan data yang memiliki *null values* di dalam *row* setiap data.

2. Normalisasi:
Tahapan ini diperlukan untuk mengubah nilai kolom numerik dalam kumpulan data ke skala umum, tanpa mendistorsi perbedaan dalam rentang nilai. Pada proyek ini, data yang dinormalisasi adalah data pada kolom rating pada file ratings.csv. Proses normalisasi dilakukan dengan metode *Min Max*.  Dimana cara kerja dari metode *Min Max* adalah setiap nilai pada sebuah fitur dikurangi dengan nilai minimum fitur tersebut, kemudian dibagi dengan rentang nilai atau nilai maksimum dikurangi nilai minimum dari fitur tersebut.

3. Melakukan *splitting* pada dataset:
Dataset akan dibagi menjadi 2, yaitu *train* dan *test data*. *Train data* digunakan sebagai *training model*, sedangkan *test data* digunakan sebagai validasi apakah model yang digunakan sudah akurat atau belum. Proposi yang umum dalam *splitting dataset* adalah 80:20, 80% sebagai *train data* dan 20% sebagai *test data*. Untuk melakukan splitting pada dataset, pertama-tama mengacak sample data. Kemudian membagi data, dimana terdapat parameter test_size yang digunakan untuk mendefinisikan ukuran data testing. Dalam contoh proyek ini, test_size=200000. Dan dilanjutkan dengan membagi data untuk modelling. Untuk modelling ini, menggunakan slicing dengan format [baris, kolom], dimana [X_train[:, 0], X_train[:, 1] berarti akan mengeksekusi semua baris, kolom pertama dan kedua.

#
## Modeling
Model yang digunakan pada proyek kali ini adalah menggunakan teknik *embedding*. Pada proyek kali ini menggunakan model *Neural Collaborative Filtering (NCF)*. Model *Neural Collaborative Filtering (NCF)* adalah jaringan saraf *(neural network)* yang menyediakan *Collaborative Filtering* berdasarkan umpan balik implisit. Secara khusus, ini memberikan rekomendasi produk berdasarkan interaksi *user* dan item. Data pelatihan untuk model ini harus berisi urutan pasangan (ID pengguna, ID anime) yang menunjukkan bahwa pengguna yang ditentukan telah berinteraksi dengan item, misalnya dengan memberi peringkat atau mengkliknya. Berikut ini merupakan langkah-langkah untuk mendapatkan *list* rekomendasi *movie* berdasarkan aktivitas *user* berdasarkan *rate* yang diberikan oleh *user*:
1. Mencari data *movie* apa saja yang telah ditonton oleh *user* lalu memasukkannya ke dalam *dataframe* yang baru.
Dimana parameter yang digunakan adalah userId, plot dengan nilai *False*, dan temp dengan nilai 1.

2. Lalu mencari *rating* terendah dari *movie*
Dimana parameter yang digunakan adalah rating_df.userId bernilai sama dengan userId.

3. Selanjutnya membuat *top_movie_refference* dengan mengurutkannya berdasarkan *rating* dari *movie*
Dimana parameter yang digunakan adalah *sort_values* dari "rating" dan *ascending* dengan nilai *False*.

4. Setelah itu saya membuat *dataframe* baru *(user_pref_df)* berdasarkan *dataframe* utama *(movie_df)* dan melakukan seleksi yang mana data yang dimasukkan adalah *movie* yang termasuk kedalam *top_movie_refference*
Dimana parameter yang digunakan adalah movie_df yang diambil dari movieId dan parameter isin yang berasal dari top_movie_refference.

5. Dan selanjutnya menghitung rata-rata *rating* yang diberikan oleh *user*
Dimana parameter yang digunakan adalah rating_df.userId bernilai sama dengan userId.

#
Pada Tabel 4, merupakan daftar 8 rekomendasi *movie* yang diperoleh dari proyek ini.

Tabel 4. Rekomendasi *Movie*
| movieId | title	                             | genres                                          |
|---------|------------------------------------|-------------------------------------------------|
| 1       | Toy Story (1995)	                 | Adventure-Animation-Children-Comedy-Fantasy     |
| 296     | Pulp Fiction (1994)	               | Comedy-Crime-Drama-Thriller                     |
| 318     | Shawshank Redemption, The (1994)   | Crime-Drama                                     |
| 356     | Forrest Gump (1994)		             | Comedy-Drama-Romance-War                        |
| 364     | Lion King, The (1994)	             | Adventure-Animation-Children-Drama-Musical-IMAX |
| 527     | Schindler's List (1993)		         | Drama-War                                       |
| 529     | Searching for Bobby Fischer (1993) | Drama                                           |
| 539  	  | Sleepless in Seattle (1993)	       | Comedy-Drama-Romance                            |

#
## Evaluation
Untuk evaluasi pada proyek kali ini adalah menggunakan *mse (mean squared error), precision,* dan *recall*.
1. MSE (Mean Squared Error) : 
Metode *Mean Squared Error* secara umum digunakan untuk mengecek estimasi berapa nilai kesalahan pada peramalan. Nilai *Mean Squared Error* yang rendah atau nilai *mean squared error* mendekati nol menunjukkan bahwa hasil peramalan sesuai dengan data aktual dan bisa dijadikan untuk perhitungan peramalan di periode mendatang. Metode *Mean Squared Error* biasanya digunakan untuk mengevaluasi metode pengukuran dengan model regresi atau model peramalan seperti *moving average, weighted moving average* dan analisis *trendline*. Cara menghitung *Mean Squared Error (MSE)* adalah dengan melakukan pengurangan nilai data aktual dengan data peramalan dan hasilnya dikuadratkan *(squared)* kemudian dijumlahkan secara keseluruhan dan membaginya dengan banyaknya data yang ada. Nilai MSE yang didapatkan dari proyek ini adalah  0.0054.

![image](https://user-images.githubusercontent.com/97511774/191566231-a8a15882-075e-47bb-b202-a243d34dbdea.png)
#### Gambar 1. Grafik MSE

Pada Gambar 1, merupakan grafik mse yang dihasilkan dari proses training model. Dimana pada grafik berwarna biru *(MSE Train)* menunjukkan penurunan. Sedangkan grafik berwarna orange *(MSE Test)* cenderung stabil.


#
2. Precission :
adalah tingkat ketepatan antara informasi yang diminta oleh user dengan jawaban yang diberikan oleh sistem. Nilai *precission* yang didapatkan dari proyek ini adalah 1.0000.

![image](https://user-images.githubusercontent.com/97511774/191566321-248266c5-c24b-4b19-9e4d-ce79056b282b.png)
#### Gambar 2. Grafik *Precission*

Pada Gambar 2, merupakan grafik *precission* yang dihasilkan dari proses training model. Dimana pada grafik berwarna biru *(Precission Train)* menunjukkan kenaikan dan cenderung stabil. Sedangkan grafik berwarna orange *(Precission Test)* cenderung stabil.

#
3. Recall : 
adalah tingkat keberhasilan sistem dalam menemukan kembali sebuah informasi. Nilai *Recall* yang didapatkan dari proyek ini adalah 0.7155. Dan untuk grafik *recall* yang dihasilkan dari proses *training model* adalah sebagai berikut:

![image](https://user-images.githubusercontent.com/97511774/191566378-39f3850d-416e-490b-8033-6e77d69c9b52.png)
#### Gambar 3. Grafik *Recall*

Pada Gambar 3, merupakan grafik *Recall* yang dihasilkan dari proses training model. Dimana pada grafik berwarna biru *(Recall Train)* menunjukkan bentuk gelombang (naik turun), tapi didominasi dengan grafik yang cenderung naik. Sedangkan grafik berwarna orange *(Recall Test)* cenderung turun dan sedikit bergelombang.

#
## Conclusion
Berdasarkan proyek yang telah dikerjakan dapat disimpulkan bahwa:
1. *Collaborative filtering* dapat digunakan untuk membuat sistem rekomendasi *movie* dengan memprediksi *rating* user terhadap *movie*
2. Nilai MSE *Mean Squared Error* yang didapatkan dari proyek ini adalah 0.0054
3. Nilai *precission* yang didapatkan dari proyek ini adalah 1.0000
4. Nilai *Recall* yang didapatkan dari proyek ini adalah 0.7155

#
## Reference
[1] F. Ajipradana, "Sistem Rekomendasi Film Menggunakan Algoritma Item-Based Collaborative Filtering dan Basis Data Graph," Universitas Diponegoro, Semarang, 2017.
