import React, { useEffect } from 'react';
import styles from './analysis.css';
import ProLayout, {
  PageContainer,
  DefaultFooter,
} from '@ant-design/pro-layout';
import menuProps from './menuProps';
import { useState } from 'react';
import BarChart from '../components/barchart'

export default function Page() {
  // Vega object
  const [spec, setSpec] = useState({});
  const [spec2, setSpec2] = useState({});
  const [spec3, setSpec3] = useState({});
  
  // Get vega object
  useEffect(()=>{
    fetch('/api/top-categories-by-sales').then(res => res.json()).then(data => {
      setSpec(data);
    });
    fetch('/api/top-categories-by-revenues').then(res => res.json()).then(data => {
      setSpec2(data);
    });
    fetch('/api/conversions').then(res => res.json()).then(data => {
      setSpec3(data);
    });
  }, []);

  return (
    <>
      <ProLayout
        {...menuProps}
        className={styles.proLayout}
      >
        <div>
          <h1 className={styles.title}>Analysis</h1>
        </div>

        <BarChart spec={spec}></BarChart>
        <BarChart spec={spec2}></BarChart>
        <BarChart spec={spec3}></BarChart>
      </ProLayout>
    </>
  );
}
