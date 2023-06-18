import "@/styles/globals.css";
import { Lato } from "next/font/google";


const lato = Lato({ subsets: ["latin"] });

export default function App({ Component, pageProps }) {
  return (
    
    <main className={lato.className}>
      <Component {...pageProps} />
    </main>
  );
}
