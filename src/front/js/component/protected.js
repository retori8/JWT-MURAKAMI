import React, { useContext } from 'react';
import { Context } from "../store/appContext";
import { Navigate } from 'react-router-dom'

export const Protected = ({ children }) => {
    const { store } = useContext(Context);
    if (store.currentUser?.token) {
        return children
    }else{
        return <Navigate to="/" />
    }
}

