import Head from "next/head";
import styles from "@/styles/Home.module.css";
import AddButton from "../components/AddButton";
import Modal from "../components/Modal";
import { useState } from "react";


export default function Home() {

  const [visible, setVisible] = useState(false);

  return (

    <>

      <Head>

        <title>K8s todo</title>
        <meta name="description" content="Microservices todo list web app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />

      </Head>

      <main className={styles.content}>

        <h1 className={styles.text} style={{marginBottom: "10px"}}>YOUR TODO LIST</h1>
        <AddButton addHandler={() => setVisible(true)} />
        { visible && <Modal setVisible={setVisible} /> }

      </main>

    </>

  );

}
