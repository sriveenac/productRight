import React, { useEffect } from 'react';
import styles from './analysis.css';
import ProLayout, {
  PageContainer,
  DefaultFooter,
} from '@ant-design/pro-layout';
import menuProps from './menuProps';
import { useState } from 'react';
import Analysis from '../components/container/analysis'

export default function Page() {
  return (
    <>
      <ProLayout
        {...menuProps}
        className={styles.proLayout}
      >
        <div className={styles.content}>
          <Analysis></Analysis>
        </div>
      </ProLayout>
    </>
  );
}
