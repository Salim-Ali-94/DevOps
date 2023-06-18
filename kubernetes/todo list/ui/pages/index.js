import Head from "next/head";
import styles from "@/styles/Home.module.css";


export default function Home() {

  return (

    <>

      <Head>

        <title>K8s todo</title>
        <meta name="description" content="Microservices todo list web app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />

      </Head>

      <main>

        <h1 className={styles.text}>YOUR TODO LIST</h1>

      </main>

    </>

  );

}
