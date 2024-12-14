library(ncdf4)

wdir <- "../Data/"

#PRUEBAS PROPIAS
#Info del tipus de part de la ciutat que hi ha en una (lat, lon) concreta
infoEstacions <- read.csv("XVPCA_info_sconcno2_2023.csv")
infoEstacions <- head(infoEstacions,68)
taulaInfoEstacions <- table(infoEstacions)
View(taulaInfoEstacions)


mesuresEstacions <- read.csv("gene_sconcno2_2023_xvpca_emep_port.csv")
View(mesuresEstacions)
variables = mesuresEstacions[0, ]
estacions = c(41.39216, 2.009802) #Aquí aniran les dades de les estacions objectiu a mesurar mostrades al kaggle
dades = c("date", "lat", "lon", "concentration") #Columnes que ha de tenir el csv a entregar
resultats <- data.frame(Date=as.character(), #Creem DataFrame on mostrar els resultats
                        lat=double(), 
                        lon=double(), 
                        concentration=double()) 
View(resultats)
cl = colnames(mesuresEstacions)[0:-1] #Obtenim  el nom totes les estacions per poder obtenir les mesures
for(i in 1:nrow(mesuresEstacions))
{
  sum = 0.0
  for(j in cl){
    if(!is.na(mesuresEstacions[[j]][i]))
    {    
      sum = sum + mesuresEstacions[[j]][i]
      
    }
  }
  conc = sum/length(cl)
  resultats[i,] <- list(mesuresEstacions$Date[i],
                        estacions[1],
                        estacions[2],
                        conc)
}
  