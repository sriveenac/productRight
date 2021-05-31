import React, { useEffect } from 'react';
import styles from './analysis.css';
import { useState } from 'react';
import BarChart from '../charts/barchart'

export default function Analysis() {
    // Vega object
    const [specTopCategoriesBySales, setSpecTopCategoriesBySales] = useState({});
    const [specTopCategoriesByConversions, setSpecTopCategoriesByConversions] = useState({});
    const [specTopBrandsBySales, setSpecTopBrandsBySales] = useState({});
    const [specTopBrandsByConversions, setSpecTopBrandsByConversions] = useState({});
    
    // Get vega object
    useEffect(()=>{
      fetch('/api/top-categories-by-sales-with-revenue').then(res => res.json()).then(data => {
        setSpecTopCategoriesBySales(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/conversions').then(res => res.json()).then(data => {
        setSpecTopCategoriesByConversions(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/top-brands-by-sales-with-revenues').then(res => res.json()).then(data => {
        setSpecTopBrandsBySales(data);
      });
    }, []);

    useEffect(() => {
      fetch('/api/top-brands-by-conversions').then(res => res.json()).then(data => {
        setSpecTopBrandsByConversions(data);
      });
    }, []);
  
    return (
      <>
        <div>
        <h1 className={styles.title}>Analysis</h1>
        </div>

        <div>
        <h2 className={styles.subtitle}>Category Level</h2>
        </div>
        <BarChart spec={specTopCategoriesBySales}></BarChart>
        <BarChart spec={specTopCategoriesByConversions}></BarChart>
        
        <div>
        <h2 className={styles.subtitle}>Brand Level</h2>
        </div>
        <BarChart spec={specTopBrandsBySales}></BarChart>
        <BarChart spec={specTopBrandsByConversions}></BarChart>
      </>
    );
  }
  