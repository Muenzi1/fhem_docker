define d_Wohnzimmer_agg dummy 

define nt_wz_clima_agg notify (ESPEasy_Kueche_BMP|ESPEasy_Wohnzimmer_BMP) {\
    \
    my $kueche_temp = ReadingsNum("ESPEasy_Kueche_BMP", "Temperature", 20, 2);;\
    my $kueche_pre = ReadingsNum("ESPEasy_Kueche_BMP", "Humidity", 1010, 2);;\
    my $kueche_hum = ReadingsNum("ESPEasy_Kueche_BMP", "Temperature", 50, 2);;\
    my $wz_temp = ReadingsNum("ESPEasy_Wohnzimmer_BMP", "Temperature", 20, 2);;\
    my $wz_pre = ReadingsNum("ESPEasy_Wohnzimmer_BMP", "Humidity", 1010, 2);;\
    my $wz_hum = ReadingsNum("ESPEasy_Wohnzimmer_BMP", "Temperature", 50, 2);;\
    \
    my $agg_temp = ($kueche_temp + $wz_temp)/2;;\
    my $agg_pre = ($kueche_pre + $wz_pre)/2;;\
    my $agg_hum = ($kueche_hum + $wz_hum)/2;;\
    \
    fhem("setreading d_Wohnzimmer_agg Temperature $agg_temp");;\
    fhem("setreading d_Wohnzimmer_agg Humidity $agg_hum");;\
    fhem("setreading d_Wohnzimmer_agg Pressure $agg_pre");;\
}

