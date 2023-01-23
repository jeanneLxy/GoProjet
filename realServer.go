package main

import(
	"fmt"
	"image"
	"image/color"
	"image/jpeg"
	"image/draw"
	"os"
	"net"
	"io/ioutil"
)
func main(){
	addr,_:=net.ResolveTCPAddr("tcp","127.0.0.1:1234")

	listener,_:=net.ListenTCP("tcp",addr)
	conn,_:=listener.AcceptTCP()

	data:=make([]image.Image,1024)
	n,_:=conn.Read(data)
	
	var nb int =20
	
	originalImage,_,_:=image.Decode(data)
	





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

