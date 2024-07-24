
import React,{ useState,useEffect } from "react";
import { Heading,Button, Card, Flex,Input} from '@chakra-ui/react'
import { useNavigate } from "react-router-dom";
import { Image } from '@chakra-ui/react'
import Cookies from 'js-cookie'
import pdimg from './pd.png'
import axios from "axios";

export default function Login(isLoggedIn){
    const [username,setUsername]=useState()
    const [password,setPassword]=useState()

    const navigate = useNavigate();
    const login = async() =>{
    const token = Cookies.get('csrftoken')
        try {
            axios.defaults.headers.common['X-CSRFToken'] = token
            const response = await axios.post('http://127.0.0.1:8000/login/', {
                username: username,
                password: password
            });
            const authToken = response.data.token; // extract the token from the response
            localStorage.setItem('token', authToken);
            navigate('/dashboard',{ replace: true });
        } catch (error) {
            console.log('error:', error.response);
            alert('Invalid username or password');
        }
        
    }

    return(
        <>
        <Flex justifyContent="center" alignItems="center" w="100%" h="100vh">
        <Card margin={100} p={20} justifyContent={'center'} boxShadow='2xl'>
            <Heading alignContent={'center'} textAlign= 'center'>SocialEye</Heading>
            <Flex justifyContent="center" mt={5} alignItems="center" h="100%">
            <Image src={'https://imgs.search.brave.com/ZvIJ--_2FtGiQ4uLIn0gw2HdhLchvWXIj52gdZkQcWQ/rs:fit:1200:1200:1/g:ce/aHR0cHM6Ly8xLmJw/LmJsb2dzcG90LmNv/bS8tUFVjTHloSU4z/MkUvWDJRWU5ERk1h/U0kvQUFBQUFBQUFk/MHMvMFlpMm5Hcjdo/RFktOGJBR25HbWFT/UjV0dGZZZjRjLS1B/Q0xjQkdBc1lIUS9z/MTQ1MS9Ubi1wb2xp/Y2UtbG9nby5wbmc'} boxSize='200px' sizes="sm"  mb={5} borderRadius='full' />
            </Flex>
            
            <Input placeholder='User Name'  size='sm' onChange={(e)=>(setUsername(e.target.value))}  ></Input>
            <Input type="password" placeholder="Login" mt={4} size='sm'onChange={(e)=>(setPassword(e.target.value))}></Input>
            <Button mt={4} bg='#0f70e6' color='white' onClick={() => login()}>Login</Button>
        </Card>
        </Flex>

        </>
    )
}