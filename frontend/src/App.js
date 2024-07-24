import React from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  theme,
} from '@chakra-ui/react';
import Dashboard from './component/dashboard'
import { CSSReset } from "@chakra-ui/react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './component/login';
import Logout from './component/logout'

function App() {
  return (
    <ChakraProvider theme={theme}>
      <BrowserRouter>
        <Routes>
            <Route index element={<Dashboard/>} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/logout" element={<Logout/>}/>
        </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
