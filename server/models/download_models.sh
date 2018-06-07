# Download model for vgg_normalised.t7
mkdir wct
cd wct
wget -c -O vgg_normalised.t7 "https://www.dropbox.com/s/kh8izr3fkvhitfn/vgg_normalised.t7?dl=1"

# Download pre-trained models for relu5_1 relu4_1 relu3_1 relu2_1 relu1_1
wget -c -O models.zip "https://www.dropbox.com/s/ssg39coiih5hjzz/models.zip?dl=1"
unzip models.zip
cd .. 