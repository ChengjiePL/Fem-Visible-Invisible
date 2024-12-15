library(ncdf4)
library(pracma)
library(sf)
wdir <- "../Data/"
#PRUEBAS PROPIAS
#Info del tipus de part de la ciutat que hi ha en una (lat, lon) concreta
infoEstacions <- read.csv("XVPCA_info_sconcno2_2023.csv")
infoEstacions <- head(infoEstacions, length(infoEstacions$code))
taulaInfoEstacions <- table(infoEstacions)
View(taulaInfoEstacions)


mesuresEstacions <- read.csv("gene_sconcno2_2023_xvpca_emep_port.csv")
View(mesuresEstacions)
variables = mesuresEstacions[0, ]
estacions = list(c(41.39216, 2.009802), 
                 c(41.11588, 1.191975),
                 c(41.44398, 2.237875),
                 c(41.32177, 2.082141)) #Aquí aniran les dades de les estacions objectiu a mesurar mostrades al kaggle
dades = c("date", "lat", "lon", "concentration") #Columnes que ha de tenir el csv a entregar
resultats <- data.frame(id = integer(),
                        date=as.character(), #Creem DataFrame on mostrar els resultats
                        lat=double(), 
                        lon=double(), 
                        concentration=double()) 
View(resultats)
nearest <- list(c(), c(), c(), c())
for(i in 2:length(mesuresEstacions))
{
  mitja = mean(as.double(mesuresEstacions[[i]]), na.rm=TRUE)
  for(j in 1:length(mesuresEstacions$Date))
  {
    if(is.na(mesuresEstacions[[i]][j]))
    {
      mesuresEstacions[[i]][j] = mitja
    }
  }
}


for(i in 1:length(infoEstacions$code))
{
  for(j in 1:length(estacions))
  {
    dist = haversine(c(estacions[[j]][1], estacions[[j]][2]), c(infoEstacions[i,][["lat"]], infoEstacions[i,][["lon"]]))
    nearest[[j]][length(nearest[[j]])+1] = infoEstacions[i,][["code"]]
    nearest[[j]][length(nearest[[j]])+1] = dist
  }
}

nearestCodes <- list(c(), c(), c(), c())
for(i in 1:length(nearest))
{
  mitja = mean(as.double(nearest[[i]][seq(2,length(nearest[[i]]), by=2)]))
  for(j in seq(2, length(nearest[[1]]), by=2))
  {
    if(nearest[[i]][j] <= mitja)
    {
      nearestCodes[[i]][length(nearestCodes[[i]])+1] <- nearest[[i]][j-1] 
    }
  }
}

cl = colnames(mesuresEstacions)[0:-1] #Obtenim  el nom totes les estacions per poder obtenir les mesures
for(i in 1:nrow(mesuresEstacions))
{
  for(z in 1:length(estacions))
  {
    sum = 0.0
    for(j in cl){
      if(is.element(j, nearestCodes[[z]]))
      {    
        total = mean( mesuresEstacions[[j]][i] + mesuresEstacions[[j]][i - 1] + mesuresEstacions[[j]][i + 1])
        sum = sum + total
        
      }
    }
    conc = sum/length(cl)
    if(is.na(conc))
    {
      conc = 16.2
    }
    index = (i-1) * 4 + z
    resultats[index,] <- list(index, mesuresEstacions$Date[i],
                              estacions[[z]][1],
                              estacions[[z]][2],
                              conc)
  }
}

X = resultats$date
X = as.factor(X)
Y = resultats$concentration
windows() ; msgWindow(type="maximize")#Fem un resize de la window per mostrar la gràfica
grafic = plot(X, Y,xlab="", ylab= "Concentration", las=2)

#Escrivim els resultats en un fitxer csv
write.csv(resultats, "./resultats.csv", quote = FALSE, row.names = FALSE)


