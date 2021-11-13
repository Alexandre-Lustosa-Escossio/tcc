from numpy import True_, cos, pi, sin, sqrt, exp
import streamlit as st
import time
@st.cache(suppress_st_warning=True)
def spinner():
    spinner = st.spinner('Calculando')
    with spinner:
        time.sleep(2.5)
        st.success('Feito!')
def calcula_fator_geometria_simples(tipo_engrenagem,tipo_engrenamento,raio_pinhao,passo_diametral,raio_interm,raio_eng,diametro_ref_pinhao,larg_face):
    ang_pressao = st.number_input('Insira o valor do ângulo de pressão')
    coef_adendo_pinhao = st.number_input('Insira o valor do Coeficiente de Adendo do pinhão')
    coef_adendo_interm = st.number_input('Insira o valor do Coeficiente de Adendo da intermediária')
    if tipo_engrenagem == 'Dentes Retos':
        raio_curvatura1_eng1 = sqrt((raio_pinhao+((1+coef_adendo_pinhao)/passo_diametral))**2 - (raio_pinhao*cos(ang_pressao*pi/180))**2) - (pi/6)*cos(ang_pressao*pi/180)
        raio_curvatura2_eng1 = (raio_pinhao+raio_interm)*sin(ang_pressao*pi/180)-raio_curvatura1_eng1
        raio_curvatura1_eng2 = sqrt((raio_interm+((1+coef_adendo_interm)/passo_diametral))**2 - (raio_interm*cos(ang_pressao*pi/180))**2) - (pi/6)*cos(ang_pressao*pi/180)
        raio_curvatura2_eng2 = (raio_interm+raio_eng)*sin(ang_pressao*pi/180)-raio_curvatura1_eng2
        fator_geom_sup_eng1 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng1 + 1/raio_curvatura2_eng1)*diametro_ref_pinhao)
        fator_geom_sup_eng2 =  cos(ang_pressao*pi/180)/((1/raio_curvatura2_eng1 + 1/raio_curvatura2_eng2)*2*raio_interm)
        return raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2
    elif tipo_engrenagem == 'Dentes Helicoidais':
        coef_adendo_eng = st.number_input('Insira o valor do Coeficiente de Adendo da Engrenagem')
        fator_mp = st.number_input('Insira o valor da Razão de contato transversal')
        fator_mf = st.number_input('Insira o valor da Razão de contato axial')
        fator_nr = fator_mp%1
        fator_na = fator_mf%1
        passo_axial = st.number_input('Insira o valor do Passo axial')
        angulo_helice_base = st.number_input('Insira o valor do Ângulo de hélice de base')
        if(fator_na < (1-fator_nr)):
            l_min = (fator_mp*larg_face-fator_na*fator_nr*passo_axial)/cos(angulo_helice_base*pi/180)
        else:
            l_min = (fator_mp*larg_face-(((1-fator_na)*(1-fator_nr))*passo_axial))/cos(angulo_helice_base*pi/180)
        fator_mn = larg_face/l_min
        raio_curvatura1_eng1 = sqrt((0.5*((raio_pinhao+coef_adendo_pinhao)+(raio_pinhao-coef_adendo_interm))**2)-raio_pinhao*cos(ang_pressao*pi/180)**2)
        raio_curvatura2_eng1 = (raio_pinhao+raio_interm)*sin(ang_pressao*pi/180) - raio_pinhao
        raio_curvatura1_eng2 = sqrt((0.5*((raio_interm+coef_adendo_interm)+(raio_interm-coef_adendo_eng))**2)-raio_pinhao*cos(ang_pressao*pi/180)**2)
        raio_curvatura2_eng2 = (raio_interm+raio_eng)*sin(ang_pressao*pi/180) - raio_curvatura1_eng2
        fator_geom_sup_eng1 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng1 + 1/raio_curvatura2_eng1)*diametro_ref_pinhao*fator_mn)
        fator_geom_sup_eng2 =  cos(ang_pressao*pi/180)/((1/raio_curvatura2_eng1 + 1/raio_curvatura2_eng2)*2*raio_interm*fator_mn)
        return raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2

def calcula_fator_geometria_composto(tipo_engrenagem,raio_pinhao_1,passo_diametral_1,raio_movida_1,diametro_ref_pinhao_1,larg_face_1,raio_pinhao_2,passo_diametral_2,raio_movida_2,diametro_ref_pinhao_2,larg_face_2):
    ang_pressao = st.number_input('Insira o valor do ângulo de pressão')
    coef_adendo_pinhao_1 = st.number_input('Insira o valor do Coeficiente de Adendo do Pinhão 1')
    coef_adendo_pinhao_2 = st.number_input('Insira o valor do Coeficiente de Adendo do Pinhão 2')
    if tipo_engrenagem == 'Dentes Retos':
        raio_curvatura1_eng1 = sqrt((raio_pinhao_1+((1+coef_adendo_pinhao_1)/passo_diametral_1))**2 - (raio_pinhao_1*cos(ang_pressao*pi/180))**2) - (pi/6)*cos(ang_pressao*pi/180)
        raio_curvatura2_eng1 = (raio_pinhao_1+raio_movida_1)*sin(ang_pressao*pi/180)-raio_curvatura1_eng1
        raio_curvatura1_eng2 = sqrt((raio_pinhao_2+((1+coef_adendo_pinhao_2)/passo_diametral_2))**2 - (raio_pinhao_2*cos(ang_pressao*pi/180))**2) - (pi/6)*cos(ang_pressao*pi/180)
        raio_curvatura2_eng2 = (raio_pinhao_2+raio_movida_2)*sin(ang_pressao*pi/180)-raio_curvatura1_eng2
        fator_geom_sup_eng1 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng1 + 1/raio_curvatura2_eng1)*diametro_ref_pinhao_1)
        fator_geom_sup_eng2 =  cos(ang_pressao*pi/180)/((1/raio_curvatura2_eng1 + 1/raio_curvatura2_eng2)*diametro_ref_pinhao_2)
        return raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2
    elif tipo_engrenagem == 'Dentes Helicoidais':
        coef_adendo_movidas = st.number_input('Insira o valor do Coeficiente de Adendo das Engrenagens Movidas')
        fator_mp = st.number_input('Insira o valor da Razão de contato transversal')
        fator_mf = st.number_input('Insira o valor da Razão de contato axial')
        fator_nr = fator_mp%1
        fator_na = fator_mf%1
        passo_axial = st.number_input('Insira o valor do Passo axial')
        angulo_helice_base = st.number_input('Insira o valor do Ângulo de hélice de base')
        if(fator_na < (1-fator_nr)):
            l_min_1 = (fator_mp*larg_face_1-fator_na*fator_nr*passo_axial)/cos(angulo_helice_base*pi/180)
            l_min_2 = (fator_mp*larg_face_2-fator_na*fator_nr*passo_axial)/cos(angulo_helice_base*pi/180)
        else:
            l_min_1 = (fator_mp*larg_face_1-(((1-fator_na)*(1-fator_nr))*passo_axial))/cos(angulo_helice_base*pi/180)
            l_min_2 = (fator_mp*larg_face_2-(((1-fator_na)*(1-fator_nr))*passo_axial))/cos(angulo_helice_base*pi/180)
        fator_mn_1 = larg_face_1/l_min_1
        fator_mn_2 = larg_face_2/l_min_2
        raio_curvatura1_eng1 = sqrt((0.5*((raio_pinhao_1+coef_adendo_pinhao_1)+(raio_pinhao_1-coef_adendo_movidas))**2)-raio_pinhao_1*cos(ang_pressao*pi/180)**2)
        raio_curvatura2_eng1 = (raio_pinhao_1+raio_movida_1)*sin(ang_pressao*pi/180) - raio_pinhao_1
        raio_curvatura1_eng2 = sqrt((0.5*((raio_pinhao_2+coef_adendo_pinhao_2)+(raio_pinhao_2-coef_adendo_movidas))**2)-raio_pinhao_2*cos(ang_pressao*pi/180)**2)
        raio_curvatura2_eng2 = (raio_pinhao_2+raio_movida_2)*sin(ang_pressao*pi/180) - raio_curvatura1_eng2
        fator_geom_sup_eng1 =  cos(ang_pressao*pi/180)/((1/raio_curvatura1_eng1 + 1/raio_curvatura2_eng1)*diametro_ref_pinhao_1*fator_mn_1)
        fator_geom_sup_eng2 =  cos(ang_pressao*pi/180)/((1/raio_curvatura2_eng1 + 1/raio_curvatura2_eng2)*2*raio_pinhao_2*fator_mn_2)
        return raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2


def calcula_resistencias(tensao_flexao_pinhao, tensao_flexao_interm, tensao_flexao_eng ,tensao_superficie_eng1, tensao_superficie_eng2):
    fator_kl = st.number_input('Forneça o valor de KL',step=1e-4,format='%.4f')
    temperatura_operacao = (st.number_input('Forneça a temperatura de operação em Fahrenheit'))
    if temperatura_operacao > 250:
        fator_kt = (temperatura_operacao + 460)/620
    else:
        fator_kt = 1
    fator_kr = st.selectbox('Selecione o fator Kr' , [0.85,1.00,1.25,1.50])
    resistencia_flexao_teorica = st.number_input('Forneça a resistência à fadiga de flexão teórica em Psi')
    resistencia_flexao = (resistencia_flexao_teorica*fator_kl)/(fator_kr*fator_kt)
    fator_cl = st.number_input('Forneça o valor de Cl',step=1e-4,format='%.4f')
    fator_ch = 1
    resistencia_superficial_teorica = st.number_input('Forneça a resistência à fadiga superficial teórica em Psi')
    resistencia_superficial = (resistencia_superficial_teorica*fator_cl*fator_ch)/(fator_kt*fator_kr)
    col1,col2 = st.columns(2)
    with col1: 
        st.metric('Resistência à Fadiga de Flexão corrigida',round(resistencia_flexao,2))
        fator_seguranca_flexao_pinhao = resistencia_flexao/tensao_flexao_pinhao
        fator_seguranca_flexao_interm = resistencia_flexao/tensao_flexao_interm
        fator_seguranca_flexao_eng = resistencia_flexao/tensao_flexao_eng
        st.metric("Fator de Segurança de Flexão do Pinhão", round(fator_seguranca_flexao_pinhao,2) )
        st.metric("Fator de Segurança de Flexão da Intermediária", round(fator_seguranca_flexao_interm,2) )
        st.metric('Fator de Segurança de Flexão da Engrenagem', round(fator_seguranca_flexao_eng,2) )
    with col2:
        st.metric('Resistência à Fadiga Superfícial corrigida', round(resistencia_superficial,2))
        fator_seguranca_superficie_eng1 = resistencia_superficial/tensao_superficie_eng1
        fator_seguranca_superficie_eng2 = resistencia_superficial/tensao_superficie_eng2
        st.metric("Fator de Segurança de Superfície do 1º Engrenamento", round(fator_seguranca_superficie_eng1,2))
        st.metric("Fator de Segurança de Superfície do 2º Engrenamento", round(fator_seguranca_superficie_eng2,2))

    

def calcula_esforcos_simples(tipo_engrenagem,tipo_engrenamento):
    st.markdown("<h1 text-align:center;>Calculo das tensões de um trem de engrenagens</h1>",True)        
    c1,c2,c3 = st.columns([1,1,1])
    with c2:
        st.image('trem-engrenagem-simples.png')
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
            if tipo_engrenamento == 'Trem Simples':
                vel_linha_ref = diametro_ref_pinhao*vel_pinhao*2*pi/(2*12)
                B = ((12-indice_qualidade)**(2/3))/4
                A = 50+56*(1-B)
                fator_dinamico =(A/(A+vel_linha_ref**(1/2)))**B  
                st.metric('Fator dinâmico Kv',round(fator_dinamico,2))
            else:
                vel_linha_ref_pinhao_1 = diametro_ref_pinhao*vel_pinhao*2*pi/(2*12)
                dentes_pinhao/dentes_interm
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
        coluna1,coluna2 = st.columns(2)
        with coluna1:
            carga_axial = st.number_input('Forneça a Carga Aplicada',step=.1)
        with coluna2:
            unidade_carga = st.radio(label = '',options=('lb','N'))
        if unidade_carga == 'N':
            carga_axial = carga_axial*4.448222
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
                st.metric('Cp = ',round(coef_elastico,2))
                raio_pinhao = diametro_ref_pinhao/2
                raio_interm = (dentes_interm/passo_diametral)/2
                raio_eng = (dentes_eng/passo_diametral)/2
                fator_acab_superficial = 1
                raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2 = calcula_fator_geometria_simples(tipo_engrenagem,tipo_engrenamento,raio_pinhao,passo_diametral,raio_interm,raio_eng,diametro_ref_pinhao,larg_face)
                tensao_superficie_eng1 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face*fator_geom_sup_eng1*diametro_ref_pinhao*fator_dinamico))
                tensao_superficie_eng2 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face*fator_geom_sup_eng2*raio_interm*2*fator_dinamico))
                c1,c2 = st.columns(2)
                calcula_resistencias(tensao_flexao_pinhao, tensao_flexao_interm, tensao_flexao_eng ,tensao_superficie_eng1, tensao_superficie_eng2)
                with c1:
                    st.metric("P1 Engrenamento Pinhão-Intermediária", raio_curvatura1_eng1)
                    st.metric("P2 Engrenamento Pinhão-Intermediária", raio_curvatura2_eng1)
                    st.metric('Fator I Engrenamento Pinhão-Intermediária', fator_geom_sup_eng1)
                    st.metric("Tensão de Superfície Pinhão-Intermediária", tensao_superficie_eng1)
                with c2:
                    st.metric("P1 Engrenamento Intermediária-Engrenagem", raio_curvatura1_eng2)
                    st.metric("P2 Engrenamento Intermediária-Engrenagem", raio_curvatura2_eng2)
                    st.metric('Fator I Engrenamento Intermediária-Engrenagem', fator_geom_sup_eng2)
                    st.metric('Tensão de Superfície Intermediária-Engrenagem', tensao_superficie_eng2)


def calcula_esforcos_composto(tipo_engrenagem,tipo_engrenamento):
    st.markdown("<h1 text-align:center;>Calculo das tensões de um trem de engrenagens</h1>",True)        
    c1,c2,c3 = st.columns([1,1,1])
    with c2:
        st.image('trem-engrenagem-composto.png')
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
        dentes_pinhao_1 = st.number_input('Quantidade de Dentes do Pinhão Número 1',step=1)
        dentes_movida_1 = st.number_input('Quantidade de Dentes da Engrenagem Movida 1',step=1)
        dentes_movida_2 = st.number_input('Quantidade de Dentes da Engrenagem Movida 2')
    with col2:
        passo_diametral_1 = st.number_input('Insira o valor do passo diametral Pd do Pinhão Número 1:',step=.1)
        dentes_pinhao_2 = st.number_input('Quantidade de Dentes do Pinhão Número 2',step=1)  
        passo_diametral_2 = st.number_input('Insira o valor do passo diametral Pd do Pinhão Número 2:',step=.1)
    if passo_diametral_1 !=0 and dentes_pinhao_1 !=0 and dentes_pinhao_2 !=0 and passo_diametral_2 !=0:
        diametro_ref_pinhao_1 = dentes_pinhao_1/passo_diametral_1 
        diametro_ref_pinhao_2 = dentes_pinhao_2/passo_diametral_2
        larg_face_1 = 12/passo_diametral_1 #inches
        larg_face_2 = 12/passo_diametral_2
        diametro_ref_movida_1 = dentes_movida_1/passo_diametral_1
        diametro_ref_movida_2 = dentes_movida_2/passo_diametral_2
        c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1,2,1,2,1,2,1,2])
        with c1:
            st.latex(r'''d_{p1} =''')
        with c2:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_pinhao_1,2)),True)
        with c3:
            st.latex(r'''d_{mov1} =''')
        with c4:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_movida_1,2)),True)
        with c5:
            st.latex(r'''d_{p2} =''')
        with c6:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_pinhao_2,2)),True)   
        with c7:
            st.latex(r'''d_{mov2} =''')
        with c8:
            st.markdown("""
            <h3>{}</h3>
            """.format(round(diametro_ref_movida_2,2)),True)    
        if larg_face_1 != 0 and larg_face_2 != 0:
            vel_pinhao_1 = st.number_input('Velocidade angular do pinhão em RPM',step=.5)
            fator_aplicacao = st.selectbox('Selecione o Fator de Aplicação KA',
            [1.00,1.25,1.5,1.75,2.00,2.25])
            fator_distribuicao = st.selectbox('Selecione o Fator de Distribuição de Carga KM',
            [1.6,1.7,1.8,2.0])
            indice_qualidade = st.number_input('Insira o valor do índice de qualidade Qv',step=.1)
            vel_pinhao_2 = vel_pinhao_1 * (dentes_pinhao_1/dentes_movida_1)
            vel_linha_ref_pinhao_1 = diametro_ref_pinhao_1*vel_pinhao_1*2*pi/(2*12)
            vel_linha_ref_pinhao_2 = diametro_ref_pinhao_2*vel_pinhao_2*2*pi/(2*12)
            B = ((12-indice_qualidade)**(2/3))/4
            A = 50+56*(1-B)
            fator_dinamico_1 = (A/(A+vel_linha_ref_pinhao_1**(1/2)))**B
            fator_dinamico_2 = (A/(A+vel_linha_ref_pinhao_2**(1/2)))**B
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
        colu1,colu2 = st.columns(2)
        with colu1:
            fator_geometria_flexao_pinhao_1 = st.number_input('Determine o fator de flexão do Pinhão 1 (J)')
            fator_geometria_flexao_pinhao_2 = st.number_input('Determine o fator de flexão do Pinhao 2 (J)')
        with colu2:
            fator_geometria_flexao_movida_1 = st.number_input('Determine o fator de flexão da Engrenagem Movida 1 (J)')
            fator_geometria_flexao_movida_2 = st.number_input('Determine o fator de flexão da Engrenagem Movida 2 (J)')
        carga_axial = st.number_input('Forneça a Carga Aplicada',step=.1)
        if (carga_axial !=0) and (fator_geometria_flexao_pinhao_1 != 0) and (fator_geometria_flexao_pinhao_2 != 0) and (fator_geometria_flexao_movida_1 != 0 and fator_geometria_flexao_movida_2) :
            spinner()  
            tensao_flexao_pinhao_1 = carga_axial*passo_diametral_1*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face_1*fator_geometria_flexao_pinhao_1*fator_dinamico_1)
            tensao_flexao_movida_1 = carga_axial*passo_diametral_1*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face_1*fator_geometria_flexao_movida_1*fator_dinamico_1)
            tensao_flexao_pinhao_2 = carga_axial*passo_diametral_2*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face_2*fator_geometria_flexao_pinhao_2*fator_dinamico_2) 
            tensao_flexao_movida_2 = carga_axial*passo_diametral_2*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_borda*fator_ciclocarga/(larg_face_2*fator_geometria_flexao_movida_2*fator_dinamico_2)
            st.latex(r'''
            \sigma = \frac{W_t K_a K_m K_s K_B K_t}{FmJK_v}
            ''')
            c1,c2 = st.columns(2)
            with c1:
                st.metric('Tensão de Flexão no Pinhão 1', round(tensao_flexao_pinhao_1,2))
                st.metric('Tensão de Flexão na Engrenagem Movida 1',round(tensao_flexao_movida_1,2))
            with c2:    
                st.metric('Tensão de Flexão no Pinhão 2',round(tensao_flexao_pinhao_2,2))    
                st.metric('Tensão de Flexão na Engrenagem Movida 2',round(tensao_flexao_movida_2,2))
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
                raio_pinhao_1 = diametro_ref_pinhao_1/2
                raio_pinhao_2 = diametro_ref_pinhao_2/2
                raio_movida_1 = (dentes_movida_1/passo_diametral_1)/2
                raio_movida_2 = (dentes_movida_2/passo_diametral_2)/2
                fator_acab_superficial = 1
                raio_curvatura1_eng1,raio_curvatura1_eng2,raio_curvatura2_eng1,raio_curvatura2_eng2,fator_geom_sup_eng1,fator_geom_sup_eng2 = calcula_fator_geometria_composto(tipo_engrenagem,raio_pinhao_1,passo_diametral_1,raio_movida_1,diametro_ref_pinhao_1,larg_face_1,raio_pinhao_2,passo_diametral_2,raio_movida_2,diametro_ref_pinhao_2,larg_face_2)
                tensao_superficie_eng1 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face_1*fator_geom_sup_eng1*diametro_ref_pinhao_1*fator_dinamico_1))
                tensao_superficie_eng2 = coef_elastico*sqrt((carga_axial*fator_aplicacao*fator_distribuicao*fator_tamanho*fator_acab_superficial)/(larg_face_2*fator_geom_sup_eng2*raio_pinhao_2*2*fator_dinamico_2))
                c1,c2 = st.columns(2)
                resistencia_flexao, resistencia_superficial = calcula_resistencias()
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
                            

def main():
    tipo_engrenagem = st.sidebar.selectbox('Selecione o tipo de engrenagem',('Dentes Retos', 'Dentes Helicoidais'))
    tipo_engrenamento = st.sidebar.selectbox('Selecione o tipo de engrenamento',('Trem Simples','Trem Composto'))
    if tipo_engrenamento == 'Trem Simples':
        calcula_esforcos_simples(tipo_engrenagem,tipo_engrenamento)
    else:
        calcula_esforcos_composto(tipo_engrenagem,tipo_engrenamento)


if __name__ == "__main__":
    main()


""" numero_estagios = (st.number_input('Numero de estagios',format = '%i',step=1))
numero_engrenagens = 2*(numero_estagios-2) + 2
razao_engrenamento = st.number_input('Determine a razão de engrenamento')
engrenagens = {}
engrenagens[0] = st.number_input('Determine o número de dentes da engrenagem 0')
if numero_estagios != 0:
    for i in range(1,int(numero_engrenagens+1),2):
        engrenagens[i] = engrenagens[i-1]*razao_engrenamento
        engrenagens[i+1] = engrenagens[i-1]
    st.write(razao_engrenamento)    
    st.write(engrenagens) """