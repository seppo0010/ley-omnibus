import React from "react"


import Layout from "../components/layout"
import SEO from "../components/seo"


const Proyecto = () => {


    return (
        <Layout>
            <SEO title="Acerca del Proyecto"/>
            <div className="mt-10 md:mt-20 flex flex-col w-10/12 md:w-2/3 text-justify mx-auto my-auto h-auto font-sans">

                <p className="mb-1">Adaptación de <a
                    href={"https://resistencia.uy/"}
                    target="_blank"
                    rel="noopener noreferrer">LOC Comparada</a> a la ley Ómnibus. <a
                    href={"https://github.com/seppo0010/ley-omnibus/"}
                    target="_blank"
                    rel="noopener noreferrer">Ver código fuente</a>.</p>

            </div>


        </Layout>
    )

}

export default Proyecto

