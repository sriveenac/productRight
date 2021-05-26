import React from 'react';
import BarChart from '../charts/barchart';
import styles from './recommendation.css';
import { useState, useEffect } from 'react';

export default function Recommendation() {
    // Vega object
    const [specNearestItems, setSpecNearestItems] = useState({});
    
    // Get vega object
    useEffect(()=>{
      fetch('/api/nearest-items').then(res => res.text()).then(data => {
        setSpecNearestItems(data);

        document.getElementById('table').innerHTML = data;
      });
    }, []);

    return (
        <div>
            <h1 className={styles.title}>Recommendation</h1>
            <div id='table'></div>
        </div>
    );
}