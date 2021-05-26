import React from 'react';
import styles from './recommendation.css';import ProLayout, {
  PageContainer,
  DefaultFooter,
} from '@ant-design/pro-layout';
import menuProps from './menuProps';
import Recommendation from '../components/container/recommendation'

export default function Page() {
  return (
    <>
      <ProLayout
        {...menuProps}
        className={styles.proLayout}
      >
        <div>
          <Recommendation></Recommendation>
        </div>
      </ProLayout>
    </>
  );
}
