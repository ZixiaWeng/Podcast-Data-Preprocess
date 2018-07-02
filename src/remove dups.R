# Remove duplicated podcast urls after Step 2 scrape
darwin_urls = read.csv("itunes-podcast-list.csv", header=FALSE)
undup_darwin_urls = darwin_urls[!duplicated(darwin_urls),]
write.csv(undup_darwin_urls, file="itunes-podcast-list-UNDUP.csv")