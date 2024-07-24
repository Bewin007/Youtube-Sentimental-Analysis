import React from "react";
import { Card,Avatar,Text,Input, Center } from '@chakra-ui/react'
import {Heading } from '@chakra-ui/react'
import { AspectRatio } from '@chakra-ui/react';
import { HStack,Image,Button,Box,Flex } from "@chakra-ui/react";


export default function logout(){
    
    return(
<>

        <Flex justifyContent="center" alignItems="center" w="100%" h="100vh" bg='#353740'>
            <Card margin={90} p={20} justifyContent={'center'} boxShadow='2xl'>
                <Heading>Logout Successful</Heading>
            </Card>
        </Flex>

        </>
    )
}