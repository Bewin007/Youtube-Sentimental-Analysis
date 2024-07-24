import React, { useState,useEffect } from "react";
import {Avatar,Text,Input, Center, Heading,Link,  HStack,Image,Button,Box,Flex, Switch, useColorMode,Stack, AspectRatio  } from '@chakra-ui/react'
import img from './img.png'
import axios from 'axios';
import mapboxgl from 'mapbox-gl';
import Map from './map'
import PieChart from './piechart'


mapboxgl.accessToken = 'pk.eyJ1IjoiYmV3aW4wMDciLCJhIjoiY2xma3h0ZXMzMGZtZjNxbHEzOGF5ZmpkeCJ9.aIme4c3n0jIx0zIjgZIqhg';

export default function Dashboard() {
      
    // const [data,setData ] = useState()
    // const [piedata,setPiedata] = useState()
    // const [chartData, setChartData] = useState({});
    // const navigate = useNavigate();
    // const [scrollBehavior, setScrollBehavior] = React.useState('inside')
    // const [isLoading, setIsLoading] = useState(false);
    // const [validate, setValidate] = useState(false)
    // const [ profile,setprofile] = useState()
    // const [ showchart,setShowchart] = useState(false)


    const [chat , setchat] = useState()
    const { colorMode, toggleColorMode } = useColorMode();
    const [isDark, setIsDark] = useState(colorMode === "dark")
    const [url, setUrl] = useState('');
    const [products, setProducts] = useState([]);
    const [embeded,setEmbeded] = useState()
    const [content,setContent] = useState()
    const [longitude,setLongitude] = useState(0)
    const [latitude,setAltitude] = useState(0)
    const [ismap,setIsmap] = useState()
    const [channeldata, setChanneldata] = useState()
    const [showchanneldata,setshowchanneldata] = useState(false)
    const [video , setvideo] = useState()
    const [ similarvideosdata, setsimilarvideosdata] = useState()

    let lat,lon
    let t
    let data




    const videoChart = async(t) => {
      console.log(url)
      try {
        console.log(t)
          const response = await axios.post('http://127.0.0.1:8000/video/',{video_url:url});
          
          let a = response.data
          data = response.data;
          let b = a.positive
          let c = a.negative
          let d = a.neutral
          console.log(data)
          setvideo(
          <Box  >
            <Heading>Video </Heading>
          <PieChart data={[
            { title: 'positive', value: b, color: 'green' },
            { title: 'neutral', value: d, color: 'blue' },
            { title: 'negative', value: c, color: 'red' },

          ]} /></Box>)
        } catch (error) {
          console.error(error);
        }
  }
    
      const CommentChart = async(t) => {
        try {
          console.log(t)
            const response = await axios.post('http://127.0.0.1:8000/chat/',{video_id:t});
            let a = response.data
            data = response.data;
            let b = a.positive
            let c = a.negative
            let d = a.neutral
            console.log(data)
            setchat(
            <Box  >
              <Heading>Comments </Heading>
            <PieChart data={[
              { title: 'positive', value: b, color: 'green' },
              { title: 'neutral', value: d, color: 'blue' },
              { title: 'negative', value: c, color: 'red' },
            ]} /></Box>)
          } catch (error) {
            console.error(error);
          }
    }
      
    const similarvideos = async(t) => {
      const res = await axios.post(`http://127.0.0.1:8000/similarvideo/`,{video_id:t})

      setsimilarvideosdata(res.data)
      
    }


    async function fetchProducts() { 
        
        const regex = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})/;
        const match = url.match(regex);
        t = (match ? match[1] : null);
        setEmbeded("https://www.youtube.com/embed/"+t);
        await new Promise(resolve => setTimeout(resolve, 0));
        setChanneldata(products.channel_data)
        try {
            setchat( <Heading>Calculating Comments</Heading> )
            setvideo(<Heading>Calculating Video</Heading> )
          const res = await axios.post(`http://127.0.0.1:8000/metadata/`,{video_id:t}).then(setContent(true),setshowchanneldata(false))
          const products = res.data;
          setProducts(res.data)
          
          
          if ((products.latitude) !='Nil' && (products.longitude)!='Nil') {
            setLongitude(parseFloat(products.longitude));
            setAltitude(parseFloat(products.latitude));
            lat = products.latitude;
            lon = parseFloat(products.longitude);
            setIsmap(true);
            console.log(lat, lon);
          } else {
            setLongitude(0);
            setAltitude(0);
            setIsmap(false);
          }
          
          
        } catch (err) {
          setContent(false)
          console.log(err);
        }
        // CommentChart(t)
        videoChart(url)
        // similarvideos(t)
      };
      
      


    const btnRef = React.useRef()
    const handleToggle = () => {
        toggleColorMode();
        setIsDark(!isDark);
      };



        async function show_channel_data(){
            setChanneldata(products.channel_data)
            console.log(channeldata)
            setshowchanneldata(!showchanneldata)
            console.log(showchanneldata)
        }


    return(
        <>
        <Box boxShadow='lg' direction='row' display='flex' alignItems='center' pl='5' pr='5' pt='3' pb='3' borderBottom='md'>
            <Avatar src={img} objectFit='above'  boxSize="70px" ></Avatar>
            <Heading fontSize='25' ml='3'>SocialEye</Heading>
            <Switch size='md' isChecked={isDark} marginLeft='auto' onChange={handleToggle}/>
            <Text p='4'fontSize='20'>Dark</Text>
        </Box>

        <Box m='5' ml='6' mr='6' >
            <br></br>
            <Text fontSize='20' ml='10'mr='10'>SocialEye grabs singular details about a video and its uploader and its creator, or channel.</Text>
            <br></br>
            <Text fontSize='20' ml='10'mr='10'>Submit link or id to a video</Text>
        </Box>
        
        <Flex m='5' ml='59' mr='59'>
            <HStack w='100%' >
                <Input placeholder = "Enter the URL" onChange={(e)=>{setUrl(e.target.value)}} /> 
                <Button bg='#0f70e6' color='white' onClick={(e)=>{fetchProducts(); setContent(false)}} >Search</Button>
            </HStack>
        </Flex>
        
        {content && (
        <Flex m ='5' h='100vh' id="spliter">
            <Box overflow="scroll"  w="50%" h="90vh" ml='10' mr='5' boxShadow='2xl' borderRadius='5'>

                        <Stack  spacing='4' m='4'>
                        <AspectRatio maxW='650' ratio={2} ml='5%' mt='5' mr='5%' overflow='hidden' >
                        <Image src={products.thumbnail}></Image>
                        </AspectRatio>
                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            Published Date
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.uploaddate}
                            </Text>
                        </Box>

                        <Box>

                          <Heading size='xs' textTransform='uppercase'>
                            ChannelId
                            </Heading>

                            
                            <Text pt='2' fontSize='sm'>{products.channelid}
                            </Text>
                        </Box>

                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            Title
                            </Heading>
                            <Text pt='2' fontSize='sm'>
                            {products.title}
                            </Text>
                        </Box>
                        
                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            Description
                            </Heading>
                            <Text pt='2' fontSize='sm'>
                            {products.description}
                            </Text>
                        </Box>

                        <Box>
                        <Heading size='xs' textTransform='uppercase'>
                            Similar Videos
                            </Heading>
                        {similarvideosdata && similarvideosdata.map(video => (

                              <div key={video.id}>
                                  <Link href={video}>{video}</Link>
                              </div>
                          ))}
                      </Box>



                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            Views
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.view_count}
                            </Text>
                        </Box>
                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            Likes
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.like_count}</Text>
                        </Box>
                        
                        <Box >
                            <Heading size='xs' textTransform='uppercase'>
                            Tags
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.video_tags}
                            </Text>
                        </Box>
                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            No of comments
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.comment_count}
                            </Text>
                        </Box>
                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            latitude
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.latitude}
                            </Text>
                        </Box>

                    

                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            longitude
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.longitude}
                            </Text>
                        </Box>

                        <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            Location
                            </Heading>
                            <Text pt='2' fontSize='sm'>{products.locationDescription}
                            </Text>
                        </Box>


                    

                    { <Flex m = '5'>

                    { ismap &&
                        <Map longitude={longitude } latitude={latitude} />
                    }</Flex> }
                    <Center>
                    <Box boxSize={100}>
                        
                    <Button onClick={()=>(show_channel_data())} bg='#0f70e6' color='white' >Show channel details</Button>
                    </Box>
                    </Center>
                    { showchanneldata  &&  (

                    <Box >
                    <Box>
                            <Heading size='xs' textTransform='uppercase'>
                            Profile:
                            </Heading>
                            <Image src={products.profile} pt='4'/>

                    </Box>
                    
                    <Box pt='4'><HStack>
                            <Heading size='xs' textTransform='uppercase'>
                            Location:
                            </Heading>
                            <Text  fontSize='sm'>{channeldata.country="" ?  'nil': channeldata.country}
                            </Text>
                            </HStack>
                    </Box>
                    <Box pt='4'><HStack>
                            <Heading size='xs' textTransform='uppercase'>
                            Custom URL:
                            </Heading>
                            <Text fontSize='sm'>{channeldata.customUrl}
                            </Text>
                            </HStack>
                    </Box>
                    <Box pt='4'>
                    <HStack>
                            <Heading size='xs' textTransform='uppercase'>
                            Default Language:
                            </Heading>
                            <Text  fontSize='sm'>{channeldata.defaultLanguage}
                            </Text>
                      </HStack>
                    </Box>

                      <HStack pt='4'>
                            <Heading size='xs' textTransform='uppercase'>
                            Name:
                            </Heading>
                            <Text fontSize='sm'>{channeldata.title}
                            </Text>
                      </HStack>



                    </Box>
                    )}

                    </Stack>

            </Box>
            <Box w="50%" h="90vh" p={4}  mr='10' ml='5' boxShadow='2xl' borderRadius='5' bg='transparent' overflow="auto"  >
                <AspectRatio maxW='650' ratio={2} ml='5%' mt='5' mr='5%' overflow='hidden' >
                    <iframe
                        src={embeded}
                        allowFullScreen
                    />
                </AspectRatio>
                
                <Heading size='xs' mt ='10' mb='10' textTransform='uppercase'>Content analysis:</Heading>
                <Center mt='3'>
                    <HStack >
                    </HStack>
                
                <Box mr='10%' ml='10%'  size='md'>
                    <Box  >
                    <Center>
                    
                    
                    {video}
                    </Center>
                    </Box>
                    
                    <Box  mt='50px'>
                    <Center>
                      
                    
                    {chat}
                    </Center>
                    </Box>
                </Box>
                </Center>

            </Box>
        </Flex>
    )}  


        </>
    )
}