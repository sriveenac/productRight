import styles from './index.less';
import ProLayout, {
  PageContainer,
  DefaultFooter,
} from '@ant-design/pro-layout';
import menuProps from './menuProps';
import React, { useEffect, useState } from 'react';

export default function IndexPage() {
  // Get time
  const [currentTime, setCurrentTime] = useState(0);

  // Get vega object
  const [spec, setSpec] = useState({});

  useEffect(() => {
    // Set current time
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  // Return layout
  return (
    <>
      <ProLayout
        {...menuProps}
        className={styles.proLayout}
      >
        <div>
          <h1 className={styles.title}>Page index</h1>
          <h2>Current time is: {currentTime}</h2>
        </div>
      </ProLayout>
    </>
  );
}
