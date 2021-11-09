from numpy import True_, cos, pi, sin, sqrt, exp
import streamlit as st
import time
@st.cache(suppress_st_warning=True)
def spinner():
    spinner = st.spinner('Calculando')
    with spinner:
        time.sleep(2.5)
        st.success('Feito!')
def calcula_fator_geometria(tipo_engrenagem,tipo_engrenamento,raio_pinhao,passo_diametral,raio_interm,raio_eng,diametro_ref_pinhao):
    ang_pressao = st.number_input('Insira o valor do ângulo de pressão')
    coef_adendo_pinhao = st.number_input('Insira o valor do Coeficiente de Adendo do pinhão')
    coef_adendo_interm = st.number_input('Insira o valor do Coeficiente de Adendo da intermediária')
    if tipo_engrenagem == 'Dentes Retos':
        raio_curvatura1_eng1 = sqrt((raio_pinhao+((1+coef_adendo_pinhao)/passo_diametral))**2 - (raio_pinhao*cos(ang_pressao*pi/180))**2) - (pi/6)*cos(ang_pressao*pi/180)
        raio_curvatura2_eng1 = (raio_pinhao+raio_interm)*sin(ang_pressao*pi/180)-raio_curvatura1_eng1
        raio_curvatura1_eng2 = sqrt((raio_interm+((1+coef_adendo_interm)/passo_diametral))**2 - (raio_interm*cos(ang_pressao*pi/180))**2) - (pi/6)*cos(ang_pressao*pi/180)
        raio_curvatura2_eng2 = (raio_interm+raio_eng)*sin(ang_pressao*pi/180)-raio_curvatura1_eng2
        fator_geom_sup_eng1 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng1 + 1/raio_curvatura2_eng1)*diametro_ref_pinhao)
        fator_geom_sup_eng2 =  (raio_interm+raio_eng)*sin(ang_pressao*pi/180)-raio_curvatura1_eng2
        return raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2
    elif tipo_engrenagem == 'Dentes Helicoidais':
        coef_adendo_eng = st.number_input('Insira o valor do Coeficiente de Adendo da Engrenagem')
        raio_curvatura1_eng1 = sqrt((0.5*((raio_pinhao+coef_adendo_pinhao)+(raio_pinhao-coef_adendo_interm))**2)-raio_pinhao*cos(ang_pressao*pi/180)**2)
        raio_curvatura2_eng1 = (raio_pinhao+raio_interm)*sin(ang_pressao*pi/180) - raio_pinhao
        raio_curvatura1_eng2 = sqrt((0.5*((raio_interm+coef_adendo_interm)+(raio_interm-coef_adendo_eng))**2)-raio_pinhao*cos(ang_pressao*pi/180)**2)
        raio_curvatura2_eng2 = (raio_interm+raio_eng)*sin(ang_pressao*pi/180) - raio_curvatura1_eng2
        
def calcula_resistencias(dentes_pinhao,dentes_interm,dentes_eng):
    fator_kl = st.number_input('Forneça o valor de Kl')
    fator_kt = (st.number_input('Forneça a temperatura de operação em Fahrenheit') + 460)/620
    fator_kr = st.selectbox('Selecione o fator Kr' , [0.85,1.00,1.25,1.50])
    resistencia_fadiga_teorica = st.number_input('Forneça a resistência à fadiga teórica')
    resistencia_fadiga = (resistencia_fadiga_teorica*fator_kl)/(fator_kr*fator_kt)
    st.metric('Resistência à fadiga corrigida',resistencia_fadiga)
    fator_cl = st.number_input('Forneça o valor de Cl')
    fator_ch = 1
    try:
        resistencia_superficial_teorica = st.number_input('Forneça a resistência à fadiga superficial teórica')
        resistencia_superficial = (resistencia_superficial_teorica*fator_cl*fator_ch)/(fator_kt*fator_kr)
        st.metric('Resistência à Fadiga de Superfícial', resistencia_superficial)
    except:
        pass

def calcula_esforcos(tipo_engrenagem,tipo_engrenamento):
    st.markdown("<h1 text-align:center;>Calculo das tensões de um trem de engrenagens</h1>",True)        
    c1,c2,c3 = st.columns([1,1,1])
    with c2:
        st.image('/home/alexandreescossio/Pictures/trem-engrenagem-simples.png')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Tensão de flexão:')
        st.latex(r'''
            \sigma_b = \frac{W_t K_a K_m K_s K_B K_t}{FmJK_v}
            ''')
    with col2:
        st.subheader('Tensão de superfície:')
        st.latex(r'''
            \sigma_c = C_p\sqrt{\frac{W_t C_a C_m C_s C_f}{FIdC_v}}
            ''')
    st.markdown('---')
    st.subheader('Forneça os parâmetros iniciais')    
    col1, col2 = st.columns(2)
    with col1:
        dentes_pinhao = st.number_input('Quantidade de Dentes do Pinhão',step=1)
        dentes_interm = st.number_input('Quantidade de Dentes da Engrenagem Intemediária',step=1)
    with col2:
        passo_diametral = st.number_input('Insira o valor do passo diametral Pd:',step=.1)
        dentes_eng = st.number_input('Quantidade de Dentes da Engrenagem',step=1)    
    if passo_diametral !=0 and dentes_pinhao !=0 and dentes_interm !=0 and dentes_eng !=0:
        diametro_ref_pinhao = dentes_pinhao/passo_diametral 
        larg_face = 12/passo_diametral #inches
        diametro_ref_interm = dentes_interm/passo_diametral
        diametro_ref_eng = dentes_eng/passo_diametral
        c1,c2,c3,c4,c5,c6 = st.columns([1,2,1,2,1,2])
        with c1:
            st.latex(r'''d_p =''')
        with c2:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_pinhao,2)),True)
        with c3:
            st.latex(r'''d_i =''')
        with c4:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_interm,2)),True)
        with c5:
            st.latex(r'''d_g =''')
        with c6:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_eng,2)),True)    
        if larg_face != 0:
            vel_pinhao = st.number_input('Velocidade angular do pinhão em RPM',step=.5)
            fator_aplicacao = st.selectbox('Selecione o Fator de Aplicação KA',
            [1.00,1.25,1.5,1.75,2.00,2.25])
            fator_distribuicao = st.selectbox('Selecione o Fator de Distribuição de Carga KM',
            [1.6,1.7,1.8,2.0])
            indice_qualidade = st.number_input('Insira o valor do índice de qualidade Qv',step=.1)
            vel_linha_ref = diametro_ref_pinhao*vel_pinhao*2*pi/(2*12)
            B = ((12-indice_qualidade)**(2/3))/4
            A = 50+56*(1-B)
            fator_dinamico = (A/(A+vel_linha_ref**(1/2)))**B
            fator_tamanho = st.selectbox('Selecione o valor do Fator de Tamanho Ks',
            [1.00,1.25,1.50])
            espessura_borda = st.number_input('Forneça a espessura da borda (tR), caso existente')
        if espessura_borda > 0:
            profundidade_dente = st.number_input('Forneça a Profundidade do dente')
            try:
                razao_recuo = espessura_borda/profundidade_dente
                if razao_recuo >= 0.5 and razao_recuo <= 1.2:
                    fator_borda = -2*razao_recuo + 3.4
                elif razao_recuo >1.2:
                    fator_borda = 1
            except:
                pass
        else:
            fator_borda = 1
        fator_ciclocarga = 1
        fator_ciclocarga_interm = 1.42
        colu1,colu2,colu3 = st.columns(3)
        with colu1:
            fator_geometria_flexao_pinhao = st.number_input('Determine o fator de flexão do Pinhão (J)')
        with colu2:
            fator_geometria_flexao_interm = st.number_input('Determine o fator de flexão da Engrenagem Intermediária (J)')
        with colu3:
            fator_geometria_flexao_eng = st.number_input('Determine o fator de flexão da Engrenagem Final (J)')
        carga_axial = st.number_input('Forneça a Carga Aplicada',step=.1)
        if (carga_axial !=0) and (fator_geometria_flexao_pinhao != 0) and (fator_geometria_flexao_interm != 0) and (fator_geometria_flexao_eng != 0):
            spinner()  
            tensao_flexao_pinhao = carga_axial*passo_diametral*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face*fator_geometria_flexao_pinhao*fator_dinamico)
            tensao_flexao_interm = carga_axial*passo_diametral*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga_interm/(larg_face*fator_geometria_flexao_interm*fator_dinamico)
            tensao_flexao_eng = carga_axial*passo_diametral*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face*fator_geometria_flexao_eng*fator_dinamico) 
            st.latex(r'''
            \sigma = \frac{W_t K_a K_m K_s K_B K_t}{FmJK_v}
            ''')
            c1,c2,c3 = st.columns(3)
            with c1:
                st.metric('Tensão de Flexão no Pinhão', round(tensao_flexao_pinhao,2))
            with c2:    
                st.metric('Tensão de Flexão na Intermediária',round(tensao_flexao_interm,2))
            with c3:
                st.metric('Tensão de Flexão na Engrenagem',round(tensao_flexao_eng,2))    
            st.text('Calculo do Coeficiente Elástico')
            st.latex(r'''
                        C_p = \sqrt{\frac{1}{pi[(\frac{1-v_g²}{E_p}+\frac{(1-v_g²)}{E_g})]}}
                        ''')
            col1, col2 = st.columns(2)
            with col1:
                poisson_pinhao = float(st.number_input('Insira o Coeficiente de Poisson do pinhão'))
                mod_elast_pinhao = float(st.number_input('Insira o Módulo de Elasticidade do pinhão (x10⁶)'))
            with col2:    
                poisson_eng = float(st.number_input('Insira o Coeficiente de Poisson da engrenagem') )
                mod_elast_eng = float(st.number_input('Insira o Módulo de Elasticidade da engrenagem (x10⁶)'))
            if poisson_eng !=0 and poisson_pinhao !=0 and mod_elast_eng != 0 and mod_elast_pinhao !=0 :
                coef_elastico =  (1/(pi*(((1-poisson_pinhao**2)/(mod_elast_pinhao*10**6))+((1-poisson_eng**2)/(mod_elast_eng*10**6)))))**(1/2)
                st.metric('Cp = ',coef_elastico)
                raio_pinhao = diametro_ref_pinhao/2
                raio_interm = (dentes_interm/passo_diametral)/2
                raio_eng = (dentes_eng/passo_diametral)/2
                fator_acab_superficial = 1
                raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2 = calcula_fator_geometria(tipo_engrenagem,tipo_engrenamento,raio_pinhao,passo_diametral,raio_interm,raio_eng,diametro_ref_pinhao)
                tensao_superficie_eng1 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face*fator_geom_sup_eng1*diametro_ref_pinhao*fator_dinamico))
                tensao_superficie_eng2 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face*fator_geom_sup_eng2*raio_interm*2*fator_dinamico))
                c1,c2 = st.columns(2)
                with c1:
                    st.metric("P1", raio_curvatura1_eng1)
                    st.metric("P2", raio_curvatura2_eng1)
                    st.metric('Ipi', fator_geom_sup_eng1)
                    st.metric("Sigmacp", tensao_superficie_eng1)
                with c2:
                    st.metric("P1", raio_curvatura1_eng2)
                    st.metric("P2", raio_curvatura2_eng2)
                    st.metric('Iig', fator_geom_sup_eng2)
                    st.metric('Sigmaci', tensao_superficie_eng2)
                calcula_resistencias(dentes_pinhao,dentes_interm,dentes_eng)
            

def main():
    tipo_engrenagem = st.sidebar.selectbox('Selecione o tipo de engrenagem',('Dentes Retos', 'Dentes Helicoidais'))
    if tipo_engrenagem == 'Dentes Retos':
        tipo_engrenamento = st.sidebar.selectbox('Selecione o tipo de engrenamento',('Trem Simples','Trem Composto'))
    if tipo_engrenagem == 'Dentes Helicoidais':
        tipo_engrenamento == 'Trem Simples'

    calcula_esforcos(tipo_engrenagem,tipo_engrenamento)

if __name__ == "__main__":
    main()