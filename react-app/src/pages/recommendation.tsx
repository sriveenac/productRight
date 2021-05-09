import React from 'react';
import styles from './recommendation.css';import ProLayout, {
  PageContainer,
  DefaultFooter,
} from '@ant-design/pro-layout';
import menuProps from './menuProps';

export default function Page() {
  return (
    <>
      <ProLayout
        {...menuProps}
        className={styles.proLayout}
      >
        <div>
          <h1 className={styles.title}>Recommendation</h1>
        </div>
      </ProLayout>
    </>
  );
}
