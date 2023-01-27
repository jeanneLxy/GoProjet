package main
import(
	//"io"
	"net"
	"os"
	"image"
	"image/color"
	"image/jpeg"
	"image/draw"
	//"time"
	//"fmt"
)
func main(){
	listener,_:=net.Listen("tcp",":8000")
	defer listener.Close()
	listener1,_:=net.Listen("tcp",":8080")
	defer listener1.Close()
	fo,_:=os.Create("test.jpg")
	newFile0,_:=os.Create("ImFinale.jpg")
	
	for{
	
	conn,_:=listener.Accept()
	handleConnection(conn,fo)
	//time.Sleep(5)
	var nb int=20
	
	originalFile,_:=os.Open("test.jpg")//nom de fichier à traiter
	defer originalFile.Close()
	
	originalImage,_,_:=image.Decode(originalFile)
	//découper l'image originale
	myImages:=decoupeImage(nb,originalImage)//ici on obtient n parties
	//commencement de traitement
	//c:=make(chan image.Image)
	channels:=make([] chan image.Image,nb)
	
	for i:=0;i<nb;i++ {
		channels[i]=make(chan image.Image)
		go traitementImage(myImages[i],channels[i])
	}
	
	for i:=0;i<nb;i++ {
		myImages[i]=<-channels[i]
	}
	
	ImFinale:=combineIm(myImages)
	
	//newFile0,_:=os.Create("ImFinale.jpg")
	defer newFile0.Close()
	jpeg.Encode(newFile0, ImFinale, &jpeg.Options{Quality: 100})
	
	conn1,_:=listener1.Accept()
	
	//fmt.Print("1")
	//time.Sleep(5)
	imageSent,_:=os.Open("ImFinale.jpg")
	sendFile(conn1,imageSent)
	//fmt.Print("2")
	
	}
	
	
	
	

}
func sendFile(conn1 net.Conn,file *os.File){
	buff:=make([]byte,65000)
	for{
	n,_:=file.Read(buff)
	if n==0{
	break
	}
	conn1.Write(buff[:n])
	//fmt.Print("fini!")
	}
	
	//io.Copy(conn1,file)
	conn1.Close()
	//fmt.Print("sendOver!")
}

func handleConnection(conn net.Conn,originalFile *os.File){
	defer conn.Close()
	//fo,_:=os.Create("test.jpg")
	buf:=make([]byte,1024)
	
	for{
	n,_:=conn.Read(buf)
	if n==0{
	break
	}
	originalFile.Write(buf[:n])
	//fmt.Print("fini!")
	}
	//fmt.Print("ok!")
	
}
func traitementImage(img image.Image,c chan image.Image){
	bounds:=img.Bounds()
	grayIm:=image.NewGray(bounds)
	
	for y:=bounds.Min.Y;y<bounds.Max.Y;y++ {
		for x:=bounds.Min.X;x<bounds.Max.X;x++{
			oriColor:=img.At(x,y)
			r,g,b,_:=oriColor.RGBA()
			gris:=(r*299+g*587+b*114)/1000
			grayIm.Set(x,y,color.Gray{uint8(gris>>8)})
		}
	}
	//time.Sleep(time.Duration(3)*time.Second)
	c<-grayIm
}
func decoupeImage(n int, img image.Image)[]image.Image{
	mySlice:=make([]image.Rectangle,n+1)
	mySliceImage:=make([]image.Image,n+1)
	bounds:=img.Bounds()
	for i:=0;i<n;i++ {
		mySlice[i]=image.Rect(bounds.Min.X+i*(bounds.Max.X-bounds.Min.X)/n,bounds.Min.Y,bounds.Min.X+(i+1)*(bounds.Max.X-bounds.Min.X)/n,bounds.Max.Y)
		mySliceImage[i]=img.(interface {
			SubImage(r image.Rectangle)image.Image
		}).SubImage(mySlice[i])
		
	}
	mySlice[n]=image.Rect(bounds.Min.X+(n)*(bounds.Max.X-bounds.Min.X)/n, bounds.Min.Y, bounds.Max.X, bounds.Max.Y)
	//mySlice[n-1]=image.Rect(bounds.Max.X, bounds.Min.Y, bounds.Max.X, bounds.Max.Y)
	//fmt.Println(bounds.Min.X+(n-1)*(bounds.Max.X-bounds.Min.X)/n)
	mySliceImage[n]=img.(interface {
			SubImage(r image.Rectangle)image.Image
		}).SubImage(mySlice[n-1])
	
	//fmt.Println(mySliceImage[n-1].Bounds().Dx())
	return mySliceImage
}

func combineIm(slices [] image.Image)image.Image{
	var xImage int=0
	for i:=0;i<len(slices)-1;i++ {
		xImage+=slices[i].Bounds().Dx()
	}
		//fmt.Println(slices[15].Bounds().Dx())
		//fmt.Println(xImage)
		
		
		yTaille:=slices[0].Bounds().Dy()
	bounds:=image.Rectangle{
		Min:image.Point{X:0,Y:0},
		Max:image.Point{X:xImage,Y:yTaille},	
	}
	combIm:=image.NewGray(bounds)
	
	
	draw.Draw(combIm,slices[0].Bounds(),slices[0],image.Point{X:0,Y:0},draw.Src)
	
	
	xDecalage:=slices[0].Bounds().Dx()
	
	for i:=1;i<len(slices);i++{
		draw.Draw(combIm,slices[i].Bounds(),slices[i],image.Point{X:xDecalage,Y:0},draw.Src)
		//draw.Draw(combIm,slices[i].Bounds().Add(image.Point{X:xDecalage,Y:0}),slices[i],image.Point{X:0,Y:0},draw.Src)
		xDecalage+=slices[i].Bounds().Dx()
	}
	return combIm
}


